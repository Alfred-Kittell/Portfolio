# -*- coding: utf-8 -*-
"""
Функционал для управления платой прибора "CRHone"

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
from time import sleep
from typing import Tuple
from datetime import datetime
from socket import socket, error as socket_error

# ---- INNER ----
from bo_chrone.chroneData import parseDatetime, d2x, x2d

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


class ChroneControl:
    """Класс для управления платой прибора через TCP соединение"""

    def __init__(self, host="192.168.0.1", port=1024):
        """Инициализирует новый экземпляр класса ChroneControl"""

        self.address = (host, port)
        self._sock = socket()

        # Время ожидания между командами
        self.waitRecTime = 3  # если не будет задержки, последующие команды могут "слиться"
        # Время ожидания во время сбора данных
        self.waitFileTime = 5  # если будет меньше 5, замер придёт неполным

    # ---- Управление прибором ----

    def connect(self) -> int:
        """
        Открывает соединение с TCP сервером прибора.
        Возвращает номер ошибки (errno) либо 0 если ошибок нет
        """

        self._sock = socket()
        self._sock.settimeout(200)
        result = self._sock.connect_ex(self.address)
        sleep(self.waitRecTime)  # если не будет задержки, последующие команды могут "слиться"

        return result

    def disconnect(self):
        """Закрывает соединение с TCP сервером прибора"""

        self._sock.close()

    def sleep(self) -> bytes:
        """
        Ставит флаг сна, и переводит прибор в режим сна.
        После получения команды засыпать:
            - плата закончит текущий замер (на индикаторе будет код: 70)
            - после снятия замера засыпает (на индикаторе будет код: 74)
        """

        # Отправка запроса
        message = "#SLEEP_*"
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(1)
        sleep(self.waitRecTime)

        return buffer

    def awake(self) -> bytes:
        """
        Сбрасывает флаг сна, и переводит прибор в рабочее состояние.
        Пробуждение обычно происходит до получения ответа
        """

        # Отправка запроса
        message = "#AWAKIE*"
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(1)
        sleep(self.waitRecTime)

        return buffer

    def getStatus(self) -> Tuple[dict, str]:
        """
        Запрашивает полный перечень статусов прибора.
        Рекомендуется использовать в качестве аналога PING.
        Возвращает статусы, в виде словаря и строки
        """

        # Отправка запроса
        message = "#STATE_*"
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(2)  # Прибор отдаёт байты статусов в обратном порядке!
        sleep(self.waitRecTime)

        # Расшифровка
        first = "{0:b}".format(buffer[1]).rjust(8, '0')
        second = "{0:b}".format(buffer[0]).rjust(8, '0')
        statusStr = f"{first} {second}"

        # Формирование словаря со статусами
        statusArr = [n == '1' for n in first + second]
        statusDict = {
            "Reset": statusArr[0],
            "Sleep": statusArr[1],
            "Overheat": statusArr[2],
            "DataReady": statusArr[3],
            "Status_5": statusArr[4],
            "Status_6": statusArr[5],
            "Status_7": statusArr[6],
            "DataCorrupt": statusArr[7],

            "Autosearch": statusArr[8],
            "ExceedChannel_3": statusArr[9],
            "ExceedChannel_2": statusArr[10],
            "ExceedChannel_1": statusArr[11],
            "Status_13": statusArr[12],
            "Status_14": statusArr[13],
            "Status_15": statusArr[14],
            "CycleComplete": statusArr[15]}

        return statusDict, statusStr

    def setStatus(self, first: str, second: str):
        """
        Запрос на изменение статуса.
        Только для тестирования! У платы такой команды не существует!

        Parameters
        ----------
        first: str
            Первый байт в двоичном виде (например: "01010101")
        second: str
            Второй байт в двоичном виде (например: "01010101")
        """

        # Формирование запроса
        message = "#SET_STATE*"
        data = bytearray(message, encoding="UTF-8")
        first = int(first, 2)
        second = int(second, 2)
        data.append(second)
        data.append(first)

        # Отправка запроса
        self._sock.send(data)
        sleep(self.waitRecTime)  # если не будет задержки, последующие команды могут "слиться"

    def getIndicator(self) -> str:
        """Запрашивает HEX значение с индикатора ошибок прибора (2 маленьких дисплея)"""

        # Отправка запроса
        message = "#ERROR_*"
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(1)
        sleep(self.waitRecTime)

        return hex(buffer[0])

    def setIndicator(self, value: str):
        """
        Запрос на изменение HEX значения индикатора.
        Только для тестирования! У платы такой команды не существует!
        """

        # Формирование запроса
        message = "#SET_ERROR*"
        data = bytearray(message, encoding="UTF-8")
        data.append(int(value, 16))

        # Отправка запроса
        self._sock.send(data)
        sleep(self.waitRecTime)

    def getDatetime(self) -> datetime:
        """Запрашивает системное время прибора. Регистры 0x0 - 0x7"""

        # Отправка запроса
        message = "#R_CLK_*" + chr(0)
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(9)
        sleep(self.waitRecTime)

        return parseDatetime(buffer)

    def setDatetime(self, dtime: datetime):
        """Устанавливает системное время прибора"""

        # Формирование запроса
        message = "#W_CLK_*"
        message += chr(9)
        message += chr(0)
        message += chr(d2x(dtime.second))
        message += chr(d2x(dtime.minute))
        message += chr(d2x(dtime.hour))
        message += chr(d2x(dtime.weekday()))
        message += chr(d2x(dtime.day))
        message += chr(d2x(dtime.month))
        message += chr(d2x(dtime.year - 2000))
        message += chr(10)
        data = bytes(message, encoding="UTF-8")

        # Отправка запроса (ответ не предусмотрен)
        self._sock.send(data)
        sleep(self.waitRecTime)

    def reset(self):
        """Выполняет полный сброс настроек прибора. Команда не проверялась"""

        # Отправка запроса
        message = "#RST_BO*"
        data = bytes(message, encoding="UTF-8")
        self._sock.send(data)
        sleep(self.waitRecTime)

    # ---- Действия с регистрами ----

    def getValue(self, register: int) -> int:
        """Запрашивает данные по регистру (от 0 до 128)"""

        # Отправка запроса
        message = "#I2C_R_*"
        data = bytearray(message, encoding="UTF-8")
        data.append(register)
        self._sock.send(data)

        # Получение ответа
        buffer = self._sock.recv(9)
        sleep(self.waitRecTime)

        return buffer[0]

    def setValue(self, register: int, value: int):
        """Устанавливает значение регистра"""

        # Формирование запроса
        message = "#I2C_W_*"
        message += chr(2)
        data = bytearray(message, encoding="UTF-8")
        data.append(register)
        data.append(value)

        # Отправка запроса
        self._sock.send(data)
        sleep(self.waitRecTime)

    # --- Действия с файлами ----

    def getLastFileId(self) -> str:
        """
        Запрашивает данные с регистров для определения ID
        последнего файла записанного на приборе.

        Для старого режима записи файлов на внутренний носитель.

        Данные с регистров поступают в 10-ричном виде,
        а воспринимать их нужно как двоично-десятиричные.

        ID файла составляется из 3 таких чисел
        после "00 99" идёт "01 00" (перенос в следующий регистр)
        ID = x58 x57 x56 = 00 00 00

        Returns
        -------
        str
            ID файла. Состоит из номера и нулей с левой части,
                обязательно из 6 символов (например "001806", "000006")
        """

        x58 = x2d(self.getValue(56))
        x57 = x2d(self.getValue(57))
        x56 = x2d(self.getValue(56))
        fileId = max((x58*10000 + x57*100 + x56) - 1, 0)

        return str(fileId).rjust(6, '0')

    def getFile(self, fileId="000000") -> bytes:
        """
        Запрашивает данные замера от прибора

        Parameters
        ----------
        fileId: str, optional
            ID файла. Состоит из номера и нулей с левой части,
                обязательно из 6 символов (например "001806", "000006").
            При пустом значении, вернёт последний файл по старому режиму ("").
            При значении по умолчанию, вернёт последний файл по новому режиму
        """

        fileId = self.getLastFileId() if fileId == '' else fileId

        # Отправка запроса
        message = "#SD_MEM*" + fileId
        data = bytes(message, encoding='UTF-8')
        self._sock.send(data)
        sleep(self.waitFileTime)

        # Получение первого ответа (подтверждение, что ошибки нет)
        buffer = self._sock.recv(1)
        # Если пришло "1", значит вероятно файл не готов, либо другая проблема
        if buffer[0] != 0:
            raise socket_error("Unknown Error while getting file. Code: -1")
        sleep(self.waitFileTime)

        # Получение второго ответа (данные)
        buffer = self._sock.recv(38528)

        sleep(self.waitRecTime)

        return buffer
