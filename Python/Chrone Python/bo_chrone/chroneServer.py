# -*- coding: utf-8 -*-
"""
Функционал для эмуляции платы прибора 'CRHone'
Для локальных тестов, поведение реальной платы может отличатся

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import os
import socket
import logging
import threading
from time import sleep, perf_counter
from datetime import datetime

# ---- INNER ----
from bo_chrone.logger import createLogger
from bo_chrone.chroneData import d2x, parseDatetime

# ---- LOGS ----
logName = "../logs/server_log.txt"
LOGGER = createLogger(logName, "server", logging.DEBUG)

###########################################################


class ChroneServer:
    """Класс для симуляции платы прибора. Создаёт TCP сервер"""

    def __init__(self, host="127.0.0.1", port=1024):
        """
        Инициализирует новый экземпляр класса ChroneControl

        Parameters
        ----------
        host: str, optional
            IP адрес
        port: int, optional
            Номер порта
        """

        # Внутренние параметры
        self.status = [['0' for _ in range(8)], ['0' for _ in range(8)]]
        self.error = "0x00"

        # Сетевые параметры
        self.address = (host, port)
        self.sock = socket.socket()
        self.sock.bind(self.address)
        # self.sock.settimeout(50)
        self.tag = f"Server-{port}"

        # Потоки
        self.work = False
        self.leadLoop = threading.Thread(target=self.__leadLoop__, daemon=True)
        self.workLoop = threading.Thread(target=self.__workLoop__, daemon=True)

    # ---- Потоки ----

    def __leadLoop__(self):
        """Управляющий поток, для связи с пользователем"""

        # Подвязка команд
        commands = {
            b"#STATE_*": ["getStatus", self.__getStatus__],  # Считать статус
            b"#SET_STATE*": ["setStatus", self.__setStatus__],  # Задать статус
            b"#ERROR_*": ["getError", self.__getError__],  # Считать индикатор
            b"#SET_ERROR*": ["setError", self.__setError__],  # Задать индикатор
            b"#AWAKIE*": ["awake", self.__awake__],  # Пробуждение
            b"#SLEEP_*": ["sleep", self.__sleep__],  # Сон
            b"#R_CLK_*": ["getDatetime", self.__getDatetime__],  # Считать системное время
            b"#W_CLK_*": ["setDatetime", self.__setDatetime__],  # Задать системное время
            b"#SD_MEM*": ["getFile", self.__getFile__],  # Чтение файлов
        }

        self.sock.listen(1)
        LOGGER.info("Сервер запущен", extra={"tag": self.tag})

        # Общий цикл
        while self.work:

            # Принимает соединение и блокирует приложение в ожидании сообщения от клиента
            self.conn, addr = self.sock.accept()
            LOGGER.info(f"Подключен пользователь: {addr}", extra={"tag": self.tag})

            # Обработка команд от пользователя
            while self.work:

                # Получение запроса
                data = self.conn.recv(1024)

                # Завершение
                if not data:
                    break

                # Вычленение команды из запроса
                command = data[:data.find(b'*')+1]

                # Вызов команды
                if command in commands:
                    command = commands[command]
                    LOGGER.debug(f"Поступила команда: {data} [{command[0]}]", extra={"tag": self.tag})
                    command[1](data)

                # Неизвестная команда
                else:
                    LOGGER.warning(f"Команда не распознана - {data}", extra={"tag": self.tag})

            self.conn.close()
            LOGGER.info(f"Отключён пользователь: {addr}", extra={"tag": self.tag})

        LOGGER.info(f"Сервер остановлен", extra={"tag": self.tag})
        self.sock.close()

    def __workLoop__(self):
        """Рабочий поток, для эмуляции работы платы"""

        fileGenTime = 1
        start = 0  # perf_counter()
        self.status[0][1] = '1'  # sleep
        self.error = "0x74"  # сон
        state = "сон"

        while self.work:

            # Ожидание пробуждения
            if state == "сон":
                if self.status[0][1] == '0':  # sleep
                    state = "сбор"
                    self.error = "0x25"  # сбор данных
                    start = perf_counter()
                    LOGGER.info(f"Сбор данных", extra={"tag": self.tag})

            # Имитация сбора
            if state == "сбор":
                if self.status[0][1] == '1':  # sleep
                    state = "сон"
                if perf_counter() - start > fileGenTime:
                    state = "засыпание"
                    self.status[0][3] = '1'  # DataReady
                    self.status[0][7] = '0'  # DataCorrupt
                    self.status[1][7] = '1'  # CycleComplete
                    self.error = "0x70"  # данные готовы
                    LOGGER.info(f"Данные готовы", extra={"tag": self.tag})

            # Ожидание сна
            if state == "засыпание":
                if self.status[0][1] == '1':  # sleep
                    state = "сон"

            sleep(1)

    # ---- Выполнение команд ----

    def __getStatus__(self, data: bytes):
        """Считать статус"""

        first = int("".join([s for s in self.status[1]]), 2)
        second = int("".join([s for s in self.status[0]]), 2)
        self.conn.send(bytes([first, second]))

    def __setStatus__(self, data: bytes):
        """Задать статус"""

        first = "{0:b}".format(data[-1]).rjust(8, '0')
        second = "{0:b}".format(data[-2]).rjust(8, '0')
        LOGGER.debug(f"Новый статус: {first}, {second}", extra={"tag": self.tag})
        self.status = [[i for i in first], [i for i in second]]

    def __getError__(self, data: bytes):
        """Считать индикатор"""

        self.conn.send(bytes([int(self.error, 16)]))

    def __setError__(self, data: bytes):
        """Задать индикатор"""

        self.error = hex(data[-1])
        LOGGER.debug(f"Новое значение индикатора: {self.error}", extra={"tag": self.tag})

    def __awake__(self, data: bytes):
        """Пробуждение"""

        self.status[0][1] = '0'  # sleep
        self.error = "0x75"  # выход из режима сна командой #AWAKIE*
        self.conn.send(bytes([0]))

    def __sleep__(self, data: bytes):
        """Сон"""

        self.status[0][1] = '1'  # sleep
        self.error = "0x74"  # переход в режим сна командой #SLEEP_*
        self.conn.send(bytes([0]))

    def __getDatetime__(self, data: bytes):
        """Считать системное время"""

        dtime = datetime.now()
        mess = chr(d2x(dtime.second))
        mess += chr(d2x(dtime.minute))
        mess += chr(d2x(dtime.hour))
        mess += chr(d2x(dtime.weekday()))
        mess += chr(d2x(dtime.day))
        mess += chr(d2x(dtime.month))
        mess += chr(d2x(dtime.year - 2000))
        data = bytes(mess, encoding="UTF-8")
        self.conn.send(data)

    def __setDatetime__(self, data: bytes):
        """Задать системное время"""

        buffer = data[10:]
        dtime = parseDatetime(buffer)

    def __getFile__(self, data: bytes):
        """Чтение файлов"""

        fileId = data[8:].decode("utf-8")
        fname = f"measurements/{fileId}.txt"

        if os.path.isfile(fname):
            LOGGER.debug(f"Файл: {fileId} - найден", extra={"tag": self.tag})
            self.conn.send(bytes([0]))
        else:
            LOGGER.error(f"Файл: {fileId} - не найден", extra={"tag": self.tag})
            self.conn.send(bytes([1]))
            return

        self.error = "0x71"  # считывание файла
        with open(fname, "rb") as f:
            buffer = f.read()
        self.error = "0x25"  # сбор данных
        self.status[0][3] = '0'  # DataReady
        self.status[0][7] = '0'  # DataCorrupt
        self.status[1][7] = '0'  # CycleComplete
        self.conn.send(buffer)

    # ---- Управление сервером ----

    def start(self):
        """Запускает эмулятор'"""

        self.work = True
        self.workLoop.start()
        self.leadLoop.start()

    def stop(self):
        """Останавливает эмулятор"""

        self.work = False


if __name__ == '__main__':
    s1 = ChroneServer("127.0.0.1", 1024)
    s2 = ChroneServer("127.0.0.1", 1025)
    s1.start()
    s2.start()

    while True:
        sleep(100)
