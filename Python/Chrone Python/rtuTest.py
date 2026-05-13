# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки работы modbus RTU

(С) 2024 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
from serial import Serial
import argparse

# ---- OUTER ----
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

# ---- COMMAND LINE ----
parser = argparse.ArgumentParser()
parser.add_argument('-p', "--port", type=str, default="/dev/ttyS4")
parser.add_argument('-s', '--slaveid', type=int, default=0)
parser.add_argument('-b', '--baud', type=int, default=115200)
parser.add_argument('-bs', '--bytes', type=int, default=8)
parser.add_argument('-par', '--parity', type=str, default="N")
parser.add_argument('-sb', '--bits', type=int, default=2)
parser.add_argument('-r', '--register', type=int, default=None)
args = parser.parse_args()

###########################################################


class RtuControl:
    """Класс реализующий RTU master"""

    def __init__(self, port, baud=9600, byteSize=8, parity='N', stopBits=1):
        """
        Инициализирует новый экземпляр класса RtuControl

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

    # ---- Чтение и запись ----

    def write(self, slaveID: int, address: int, value: int):
        """Записывает значение в регистр"""

        result = self.master.execute(slaveID, cst.WRITE_SINGLE_REGISTER, address, output_value=value)
        print(f"write [{value}] in [{address}]: {result}")

    def read(self, slaveID: int, address: int, count: int, func) -> list:
        """Считывает значения с регистров"""

        result = self.master.execute(slaveID, func, address, count)

        return result


def main():
    """ """

    # Параметры RTU
    port = args.port
    baud = args.baud
    byteSize = args.bytes
    parity = args.parity
    stopBits = args.bits

    # Параметры чтения
    slaveid = args.slaveid
    register = args.register

    #
    rtu = RtuControl(port, baud, byteSize, parity, stopBits)
    rtu.open()

    funcs = [
        [cst.READ_HOLDING_REGISTERS, "Holding Registers"],
        [cst.READ_INPUT_REGISTERS, "Input Registers"],
        [cst.READ_DISCRETE_INPUTS, "Discrete Inputs"],
        [cst.READ_COILS, "Coils"],
    ]

    # Чтение одного регистра
    if register:
        try:
            result = rtu.read(slaveid, register, 1, cst.READ_HOLDING_REGISTERS)
            print(f"read from [{register}]: {result}")
        except Exception as ex:
            print(f"Error - {ex}")
    # Чтение многих регистров
    else:
        for slave in range(256):
            try:
                result = rtu.read(slave, 126, 1, cst.READ_HOLDING_REGISTERS)
                print(f"slave[{slave}] read from [{register}]: {result}")
            except Exception as ex:
                print(f"slave[{slave}] Error - {ex}")
        # for func in funcs:
        #     print(f"Function - {func[1]}")
        #     for i in range(1, 200):
        #         try:
        #             result = rtu.read(slaveid, i, 1, func[0])
        #             print(f"\tread from [{i}]: {result}")
        #         except Exception as ex:
        #             print(f"\tError - {ex}")


if __name__ == '__main__':
    main()
