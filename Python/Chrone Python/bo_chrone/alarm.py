# -*- coding: utf-8 -*-
"""
Функционал для настройки и управления сигнализацией

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
from typing import List
from serial import Serial

# ---- OUTER ----
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# ---- INNER ----
from bo_chrone.logger import MODBUS_LOGGER as LOGGER
from bo_chrone.chroneData import calcAnGram, ChroneParams, ChroneMeasurement

###########################################################


class AlarmControl:
    """
    Класс реализующий RTU master.
    Предназначен для управления сигнализацией и подключения к модулям:
        - Seneca Z-10-D-OUT 5000 (модуль вывода)
        - Seneca Z-8AL 4755 (модуль ввода) (только в теории, кода пока нет)
    """

    def __init__(self, port, baud=9600, byteSize=8, parity='N', stopBits=1):
        """
        Инициализирует новый экземпляр класса AlarmControl

        Parameters
        ----------
        port: str
            Номер/адрес COM порта
        baud: int
            Скорость передачи данных
        byteSize: int
            Биты данных в каждом передаваемом символе (5, 6, 7, 8)
        parity: str
            Четность ('N', 'E', 'O', 'M', 'S')
        stopBits: int
            Размер стоповых битов (1, 1.5, 2)
        """

        self.port = port
        self.baud = baud
        self.byteSize = byteSize
        self.parity = parity
        self.stopBits = stopBits

    # ---- Внутренняя логика ----

    def __write__(self, slaveID: int, address: int, value: int):
        """Записывает значение в регистр"""

        result = self.master.execute(slaveID, cst.WRITE_SINGLE_REGISTER, address, output_value=value)
        LOGGER.info(f"write [{value}] in [{address}]: {result}")

    def __read__(self, slaveID: int, address: int, count: int) -> list:
        """Считывает значения с регистров"""

        result = self.master.execute(slaveID, cst.READ_HOLDING_REGISTERS, address, count)
        LOGGER.info(f"read from [{address}]: {result}")

        return result

    # ---- Управление соединением ----

    def open(self):
        """Открывает соединение"""

        serial = Serial(self.port, self.baud, self.byteSize, self.parity, self.stopBits, xonxoff=0)
        self.master = modbus_rtu.RtuMaster(serial)
        self.master.set_timeout(5)
        self.master.set_verbose(True)

    def close(self):
        """Закрывает соединение"""

        self.master.close()

    # ---- Управление сигнализацией ----

    def getAlarm(self, slaveID: int) -> List[bool] or None:
        """Считывает и возвращает текущую сигнализацию"""

        try:
            value = self.__read__(slaveID, 2, 1)[0]
            x2 = "{0:b}".format(value).rjust(10, '0')
            alarm = [n == '1' for n in x2]
        except Exception as ex:
            LOGGER.error(f"Ошибка при получении сигнализации! {ex}")
            return None

        return alarm

    def setAlarm(self, slaveID: int, bits: str = "0101"):
        """Устанавливает сигнализацию"""

        try:
            value = int(bits, 2)
            self.__write__(slaveID, 2, value)
        except Exception as ex:
            LOGGER.error(f"Ошибка при выставлении сигнализации! {ex}")


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def checkNullQm(measurement: ChroneMeasurement) -> bool:
    """Проверяет замер на наличие нулевых QM и NQN"""

    for channel in ['A', 'B', 'C']:
        anGram = calcAnGram(measurement, channel)
        if anGram[0].QM * anGram[0].NQN * anGram[1].QM * anGram[1].NQN == 0:
            return False

    return True


def checkSeverityLvl(params: ChroneParams, measurement: ChroneMeasurement) -> list:
    """Формирует сигнализацию по Qm для платы"""

    # Вычисление всех Qm
    values = []
    for channel in ['A', 'B', 'C']:
        anGram = calcAnGram(measurement, channel)
        values.append(anGram[0].QM)
        values.append(anGram[1].QM)
    maxQm = max(values)

    # Определение значения пользовательской уставки
    if 7 > params.userCriterion > 0:
        # 1 = Qm_pos_A  2 = Qm_neg_A  3 = Qm_pos_B  4 = Qm_neg_B  5 = Qm_pos_C  6 = Qm_neg_C
        userPoint = values[params.userCriterion-1]
    else:
        userPoint = 0

    # Определение уровня критичности
    result = [0, 0, 0, 1]
    if userPoint >= params.userPoint:
        result[1] = 1
    if maxQm >= params.firstPoint:
        result[0] = 1
    if maxQm >= params.secondPoint:
        result[2] = 1
        result[0] = 0

    return result


def computeAlarm(severity: List[list], half=False) -> str:
    """Складывает сигнализации с каждой платы в одну"""

    result = [0, 0, 0, 1]
    for s in severity:
        result[2] = min(1, result[2] + s[2])  # 0010 - second (К)
        result[0] = min(1, result[0] + s[0])  # 1000 - first (Ж)
        result[1] = min(1, result[1] + s[1])  # 0100 - user (З)
        result[3] *= s[3]                     # 0001 - work (С)

    if result[2] > 0:
        result[0] = 0

    # Сокращённая сигнализация
    if half:
        all_on = result[0] + result[1] + result[2]
        result[0] = min(1, all_on)
        result[1] = 0
        result[2] = 0

    return "".join(str(i) for i in result)
