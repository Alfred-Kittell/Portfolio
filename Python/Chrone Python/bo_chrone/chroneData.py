# -*- coding: utf-8 -*-
"""
Функционал для хранения и обработки замеров платы прибора "CRHone"

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import struct
from math import log
from typing import Tuple, List
from datetime import datetime

# ---- INNER ----
from bo_chrone.modbus import pack_i2ush, pack_p2ush

# ---- GLOBAL AND CONSTANT ----
INPUTRANGE = [  # Входной диапазон
    35000,
    17000,
    8500,
    3400,
    1700,
    850,
    340,
    170,
    85,
    35
]  # Входной диапазон

###########################################################


def b2i(data: bytes) -> List[int]:
    """Конвертирует массив byte в массив int, на один int идёт 4 byte"""

    result = []

    for i in range(len(data) // 4):
        arr = data[i*4: (i+1)*4]
        result.append(int.from_bytes(arr, "little", signed=True))

    return result


def d2x(number: int) -> int:
    """Конвертирует десятичное число в двоично-десятичное"""

    return (number // 10) << 4 | (number % 10) & 0xf


def x2d(number: int) -> int:
    """Конвертирует двоично-десятичное число в десятичное"""

    return (number >> 4) * 10 + (number & 0xf)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def parseMatrix(raw_data: bytes) -> list:
    """
    Расшифровывает матрицу из специфического представления.
    Двумерная матрица 100x32, записанная последовательно в байтовом одномерном виде
    """

    data = b2i(raw_data)
    return [data[i:i + 32] for i in range(0, len(data), 32)]


def parseDatetime(data: bytes) -> datetime:
    """
    Расшифровывает системное время прибора из специфического представления.
    На стороне прибора хранится в 7 регистрах в двоично-десятичном коде
    """

    second = x2d(data[0])
    minute = x2d(data[1])
    hour = x2d(data[2])
    # week = min(x2d(data[3]), 1)
    day = max(x2d(data[4]), 1)
    month = max(x2d(data[5]), 1)
    year = x2d(data[6]) + 2000

    return datetime(year, month, day, hour, minute, second)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#

class Groups:
    """Класс для хранения групп разбиения"""

    def __init__(self, data=None):
        """
        Инициализирует новый экземпляр класса Groups.
        По умолчанию заполняется дефолтными границами.
        Границ может быть не более 15
        """

        if data:
            self.zones = data[:15]
        else:
            self.zones = [3.16, 10, 31.6, 100, 316, 1000]

    def getGroup(self, number: float) -> int:
        """Возвращает номер группы разбиения для числа"""

        group = 0
        if number == 0:
            return group

        for g in self.zones:
            group += 1
            if number <= g:
                return group

        return group+1

    def getZone(self, group: int) -> List[float]:
        """
        Возвращает минимум и максимум группы разбиения.
        Первая группа от 0, последняя до inf.
        Нулевая группа считается отсутствием группы
        """

        if group == 0:
            return [0, 0]
        elif group == 1:
            return [0, self.zones[0]]
        elif group > len(self.zones):
            return [self.zones[-1], float("inf")]

        return [self.zones[group-2], self.zones[group-1]]


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class ChroneParams:
    """Класс хранящий параметры и настройки платы"""

    def __init__(self, mainParams: list, severityParams: list):
        """
        Инициализирует новый экземпляр класса ChroneParams

        Parameters
        ----------
        mainParams: list
            Основные параметры платы
        severityParams: list
            Значения уставок
        """

        # Параметры идентификации
        self.id = mainParams[0]
        self.name = mainParams[1]

        # Сетевые настройки
        self.port = mainParams[2]
        self.ip = mainParams[3]

        # Параметры уставок
        self.firstPoint = severityParams[0]
        self.secondPoint = severityParams[1]
        self.userPoint = severityParams[2]
        self.userCriterion = severityParams[3]


class ChroneMeasurement:
    """Класс для хранения замера прибора"""

    def __init__(self, data: bytes, path=""):
        """Инициализирует новый экземпляр класса ChroneMeasurement"""

        if path:
            with open(path, "rb") as f:
                data = f.read()

        self.dtime = parseDatetime(data[:7])
        self.settings = data[:128]
        self.ph_a = data[128:12928]
        self.ph_b = data[12928:25728]
        self.ph_c = data[25728:]

    def getRaw(self) -> bytes:
        """Возвращает замер в исходном одномерном виде"""

        data = []
        data.extend(self.settings)
        data.extend(self.ph_a)
        data.extend(self.ph_b)
        data.extend(self.ph_c)

        return bytes(data)

    def getRange(self, channel: str) -> int:
        """Возвращает входной диапазон канала. Имена каналов: 'A', 'B', 'C'"""

        ind = self.settings[ord(channel) - 36]
        ind = 4 if ind < 0 or ind > 9 else ind

        return INPUTRANGE[ind]

    def getTime(self, channel: str) -> float:
        """Возвращает счётчик времени канала. Имена каналов: 'A', 'B', 'C'"""

        start = 8*(ord(channel) - 65) + 80
        end = start + 8

        val = struct.unpack(f"<Q", self.settings[start: end])[0]

        return round(val * 2/3 * 10**-9, 1)

    def getChannelData(self, channel: str) -> list:
        """Возвращает матрицу (32x100) с данными канала. Имена каналов: 'A', 'B', 'C'"""

        if channel == 'A':
            data = parseMatrix(self.ph_a)
        elif channel == 'B':
            data = parseMatrix(self.ph_b)
        elif channel == 'C':
            data = parseMatrix(self.ph_c)
        else:
            data = []

        return data

    def getModbus(self, inputData: list, groups=None) -> list:
        """
        Подготовка замера к записи в modbus

        Parameters
        ----------
        inputData: list
            Массив данных от датчиков. Температура и влажность
        groups: Groups, optional
            Группы разбиения. По умолчанию использует дефолтные группы
        """

        if groups is None:
            groups = Groups()

        values = []

        # Дата замера (7 тегов)
        values.append(self.dtime.second)
        values.append(self.dtime.minute)
        values.append(self.dtime.hour)
        values.append(self.dtime.weekday())
        values.append(self.dtime.day)
        values.append(self.dtime.month)
        values.append(self.dtime.year)

        # Режим работы прибора (1 тег)
        values.append(self.settings[8])

        # Битовый указатель активных каналов для режима измерения (1 тег)
        values.append(self.settings[9])

        # IP адрес (4 тега)
        values.append(self.settings[32])
        values.append(self.settings[33])
        values.append(self.settings[34])
        values.append(self.settings[35])

        # Индекс последнего замера (4 тега)
        values.append(self.settings[58])
        values.append(self.settings[59])
        values.append(self.settings[60])
        values.append(self.settings[61])

        # Температура и влажность (2 тега)
        values.extend(inputData)

        # QM и NQN (24 тега)
        anData = list(calcAnGram(self, 'A'))
        anData.extend(calcAnGram(self, 'B'))
        anData.extend(calcAnGram(self, 'C'))
        anDataAll = []
        for data in anData:
            anDataAll.append(int(round(data.QM, 1) * 10))
            anDataAll.append(int(round(data.NQN, 1) * 10))

        values.extend(pack_i2ush(anDataAll))

        # Границы групп разбиения (16 тегов)
        zones = [0 for _ in range(16)]
        for ind in range(len(groups.zones)):
            zones[ind] = int(round(groups.zones[ind], 1) * 10)
        values.extend(zones)

        # PRPD (2400 тегов)
        prpd = [PRPD(self, 'A', groups, True),
                PRPD(self, 'B', groups, True),
                PRPD(self, 'C', groups, True)]
        points = []
        for item in prpd:
            points.extend(item.groups)
        values.extend(pack_p2ush(points))

        # всего 2459 тегов
        return values


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class PRPD:
    """Класс для хранения PRPD диаграмм"""

    def __init__(self, measurement, channel, groups=None, only_groups=False):
        """
        Инициализирует новый экземпляр класса PRPD

        Parameters
        ----------
        measurement: ChroneMeasurement
            Замер
        channel: str
            Имя канала. 'A', 'B', 'C'
        groups: Groups, optional
            Группы разбиения. По умолчанию использует дефолтные группы
        only_groups: bool, optional
            Записывать только группы разбиения (Для передачи по Modbus)
        """

        if groups is None:
            groups = Groups()

        self.d_range = measurement.getRange(channel)
        data = measurement.getChannelData(channel)
        t = measurement.getTime(channel)
        t = t if t != 0 else 1  # на всякий случай

        # Обход матрицы с данными
        self.A = []  # Амплитуды
        self.N = []  # Частоты следования импульсов
        self.PH = []  # Фазы
        self.groups = []  # Номера групп
        for y in range(100):
            for x in range(32):
                n = data[y][x] / t
                self.groups.append(groups.getGroup(n))
                if n != 0 and not only_groups:
                    self.A.append((x - (16 if x < 16 else 15)) * self.d_range / 16)
                    self.N.append(n)
                    self.PH.append(y * 360 / 100)

        self.size = len(self.A)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class AnGram:
    """Класс для хранения A-n диаграммы"""

    def __init__(self, amplitudes: list, impulses: list):
        """Инициализирует новый экземпляр класса AnGram"""

        self.A = amplitudes  # Амплитуд
        self.N = impulses  # Частоты следования импульсов
        self.size = len(amplitudes)  # Число строк
        self.QM = self.__getQM()    # Наибольшая повторяющаяся амплитуда ЧР
        self.NQN = self.__getNQN()  # Нормализованная гистограмма импульсов

    def __getQM(self, find=10) -> float:
        """Находит наибольшую повторяющую амплитуду ЧР в точке пересечения с границей"""

        # Поиск первого пересечения границы
        for ind in range(1, self.size):
            if self.N[ind-1] >= find >= self.N[ind] or self.N[ind-1] <= find <= self.N[ind]:
                start = 0 if ind == 0 else ind-1
                return linear(find, self.N[start], self.A[start], self.N[ind], self.A[ind])

        return 0.0

    def __getNQN(self) -> float:
        """Рассчитывает нормализованную гистограмму импульсов"""

        if len(self.A) == 0 or len(self.N) == 0:
            return 0

        NQN = self.A[0] * log(max(1, self.N[0]))

        for ind in range(1, self.size):
            NQN += (self.A[ind] - self.A[ind-1]) * log(max(1, self.N[ind]))

        return NQN


def linear(x, x0, y0, x1, y1) -> float:
    """
    Рассчитывает линейную интерполяцию между двумя точками

    Parameters
    ----------
    x: float
        Искомая точка по оси X
    x0: float
        Координата X первой точки
    y0: float
        Координата Y первой точки
    x1: float
        Координата X второй точки
    y1: float
        Координата Y второй точки
    """

    if x1 - x0 == 0:
        return (y0 + y1) / 2
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def calcAnGram(measurement, channel, rowsIgnore=0) -> Tuple[AnGram, AnGram]:
    """
    Рассчитывает A-n диаграммы для частот положительных и отрицательных импульсов с канала

    Parameters
    ----------
    measurement: ChroneMeasurement
        Данные замера
    channel: str
        Имя канала. 'A', 'B', 'C'
    rowsIgnore: int, optional
        Число строк для удаления (от центра в обе стороны)

    Returns
    -------
    tuple[AnGram, AnGram]
        Массив с двумя A-n диаграммами (положительная и отрицательная)
    """

    d_range = measurement.getRange(channel)
    data = measurement.getChannelData(channel)
    t = measurement.getTime(channel)
    t = t if t != 0 else 1  # на всякий случай

    # Обход матрицы с данными
    a_pos = []
    n_pos = []
    a_neg = []
    n_neg = []
    for x in range(32):
        # Отсекание ненужных строк (от центра)
        if 16 - rowsIgnore <= x < rowsIgnore + 16:
            continue

        y_max = max([data[y][x] / t for y in range(100)])
        # Отсекание пустых строк
        #if y_max == 0:
        #    continue

        if x < 16:
            # Отрицательные импульсы, изначально в обратном порядке
            a_neg.insert(0, abs((x-16) * d_range / 16))
            n_neg.insert(0, y_max)
        else:
            # Положительные импульсы
            a_pos.append((x-15) * d_range / 16)
            n_pos.append(y_max)

    return AnGram(a_pos, n_pos), AnGram(a_neg, n_neg)

