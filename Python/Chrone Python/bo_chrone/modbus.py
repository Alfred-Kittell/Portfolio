# -*- coding: utf-8 -*-
"""
Функционал для работы сервера Modbus TCP

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
from typing import List

# ---- OUTER ----
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

# ---- INNER ----
from bo_chrone.logger import MODBUS_LOGGER as LOGGER

###########################################################


class ModbusServer:
    """Класс реализующий TCP slave"""

    def __init__(self, host="127.0.0.1", port=502):
        """Инициализирует новый экземпляр класса ModbusServer"""

        slaveID = 1
        self.server = modbus_tcp.TcpServer(port, host)
        self.slave = self.server.add_slave(slaveID)
        self.slave.add_block('0', cst.HOLDING_REGISTERS, 0, 10000)

    # ---- Управление соединением ----

    def start(self):
        """Запускает сервер"""

        self.server.start()
        LOGGER.info("Start TCP Slave")

    def stop(self):
        """Останавливает сервер"""

        self.server.stop()
        LOGGER.info("Stop TCP Slave")

    # ---- Управление данными ----

    def write(self, address: int, values: List[int]):
        """Записывает данные в регистры, начиная с выбранного"""

        LOGGER.debug(f"Write to TCP Slave {len(values)} values from {address} addr to Holding Registers")

        for ind in range(len(values)):
            self.slave.set_values('0', address+ind, values[ind])

    def read(self, address: int, count: int) -> list:
        """Читает данные с регистров, начиная с выбранного"""

        return self.slave.get_values('0', address, count)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def pack_i2ush(data: list) -> list:
    """
    Преобразовывает массив int в массив ushort.
    Размер массива увеличивается в 2 раза.
    Каждый элемент из исходного массива, разделяется побайтово на 2 отдельных числа
    Порядок от старшего к младшему (big-endian)
    """

    pack = []
    for n in data:
        pack.append(n >> 16)
        pack.append(n & 0xffff)

    return pack


def pack_p2ush(data: list) -> list:
    """
    Преобразовывает массив int в массив ushort.
    Размер массива уменьшается в 4 раза.
    Каждые 4 элемента из исходного массива, преобразовываются в 1 элемент конечного.
    Берутся только первые 4 бита каждого исходного числа.

    Эти преобразования нужны для сокращения итогового размера массива
    """

    pack = []
    for ind in range(0, len(data), 4):
        x1 = data[ind+0] << 12
        x2 = data[ind+1] << 8
        x3 = data[ind+2] << 4
        x4 = data[ind+3]
        pack.append(x1+x2+x3+x4)

    return pack


def unPack_i2ush(data: list) -> list:
    """
    Преобразовывает массив ushort в массив int.
    Размер массива уменьшается в 2 раза.
    Каждые 2 элемента из исходного массива, складываются побитово в 1 элемент конечного.
    Порядок от старшего к младшему (big-endian)

    Эти преобразования нужны для восстановления после операции упаковки
    """

    pack = []
    for ind in range(0, len(data), 2):
        pack.append((data[ind] << 16) + data[ind+1])

    return pack


def unPack_p2ush(data: list) -> list:
    """
    Преобразовывает массив ushort в массив int.
    Размер массива увеличивается в 4 раза.
    Каждый элемент из исходного массива, преобразовываются в 4 элемента конечного.
    На каждое число итогового массива приходиться 4 бита исходного числа (от 0 до 16)

    Эти преобразования нужны для восстановления после операции упаковки
    """

    pack = []
    for n in data:
        pack.append((n & 61440) >> 12)
        pack.append((n & 3840) >> 8)
        pack.append((n & 240) >> 4)
        pack.append(n & 15)

    return pack
