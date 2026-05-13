# -*- coding: utf-8 -*-
"""
Демон для периодического опроса прибора

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import os
import logging
import argparse
import threading
from typing import Tuple
from datetime import datetime
from time import sleep, perf_counter
from concurrent.futures import ThreadPoolExecutor

# ---- OUTER ----
import psutil

# ---- INNER ----
from bo_chrone.logger import createLogger, updatePath, MODBUS_LOGGER
from bo_chrone.chroneData import ChroneParams, ChroneMeasurement
from bo_chrone.chroneServer import ChroneServer
from bo_chrone.chroneControl import ChroneControl
from bo_chrone.postgres import PostgresControl
from bo_chrone.modbus import ModbusServer
from bo_chrone.alarm import AlarmControl, checkNullQm, checkSeverityLvl, computeAlarm

# ---- COMMAND LINE ----
parser = argparse.ArgumentParser()
parser.add_argument("--psql_pwd", default="sa211222")  # admin
parser.add_argument("--psql_user", default="postgres")
parser.add_argument("--psql_base", default="chrone")
parser.add_argument("--psql_host", default="localhost")
parser.add_argument("--psql_port", default="5432")
parser.add_argument("--alarm_port", default="")
parser.add_argument("--test", action="store_true", default=False)
args = parser.parse_args()

# ---- LOGS ----
logName = "logs/demon"
logPath = f"{logName} - {datetime.now().strftime('%y.%m')}.log"
LOGGER = createLogger(logPath, "main_log", logging.DEBUG)
createLogger(logPath, logger=MODBUS_LOGGER, level=logging.DEBUG, tag="Modbus")

# ---- GLOBAL AND CONSTANT ----
MODES = {}  # Режимы работы плат

###########################################################


def saveToFile(data, path):
    """Сохранение данных в файл с проверкой на наличие пути"""

    # Создание пути к файлу, если он не существует
    dirPath = os.path.dirname(path)
    if dirPath and not os.path.exists(dirPath):
        os.makedirs(dirPath)

    # Запись
    with open(path, 'bw') as f:
        f.write(data)


def checkEnd(path) -> bool:
    """Проверка на ручное завершение демона, содержание файла неважно"""

    if os.path.exists(path):
        return True

    return False


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def fakeThread(params: ChroneParams, baseTime: int) -> Tuple[ChroneParams, ChroneMeasurement]:
    """ """

    extra = {"tag": params.name}

    LOGGER.info(f"The board connection: {params.ip} [{params.port}]", extra=extra)
    chrone = ChroneControl(params.ip, params.port)
    start = perf_counter()
    measurement = None
    path = "backup_measurements"

    # Опрос
    while perf_counter() - start < baseTime:
        try:
            sleep(15)

            # Считывание замера
            files = os.listdir(path)

            with open(f"{path}//{files[MODES[params.id]]}", "br") as f:
                measurement = ChroneMeasurement(f.read())
                measurement.dtime = datetime.now()

            if MODES[params.id]+1 >= len(files):
                MODES[params.id] = 0
            else:
                MODES[params.id] += 1

            break
        except Exception as ex:
            chrone.disconnect()
            LOGGER.critical(f"{ex}. Re-polling after 5 minutes", extra=extra)
            #break
            sleep(300)  # 5 минут, время среднего переопроса

    chrone.disconnect()
    LOGGER.info("Stopped polling the board", extra=extra)

    return params, measurement


def pollThread(params: ChroneParams, baseTime: int) -> Tuple[ChroneParams, ChroneMeasurement]:
    """Опрос платы для получения замера"""

    MODES[params.id] = "poll"
    extra = {"tag": params.name}

    LOGGER.info(f"The board connection: {params.ip} [{params.port}]", extra=extra)
    chrone = ChroneControl(params.ip, params.port)
    start = perf_counter()
    attemptsQmCheck = 0
    measurement = None

    # Опрос
    while perf_counter() - start < baseTime:
        try:
            chrone.connect()

            # Проверка на сон и пробуждение
            status = chrone.getStatus()
            if status[0]["Sleep"]:
                LOGGER.info("The board awakens...", extra=extra)
                for i in range(5):
                    chrone.awake()
                    status = chrone.getStatus()
                    indicator = chrone.getIndicator()
                    LOGGER.debug(f"Status: {status[1]}, Indicator: {indicator}", extra=extra)
                    if not status[0]['Sleep']:
                        LOGGER.info("The board is awakened", extra=extra)
                        break
                    else:
                        sleep(5)  # 5 секунд, ожидание
            if status[0]["Sleep"]:
                raise Exception("The board isn't awake!")

            # Ожидание готовности замера
            LOGGER.info("Waiting for measurement...", extra=extra)
            while perf_counter() - start < baseTime:
                status = chrone.getStatus()
                indicator = chrone.getIndicator()
                LOGGER.debug(f"Status: {status[1]}, Indicator: {indicator}", extra=extra)
                if status[0]["DataReady"]:
                    LOGGER.info("Measurement is ready!", extra=extra)
                    break
                else:
                    sleep(15)  # 15 секунд, время быстрого переопроса

            # Проверка, что данные можно снимать
            if not status[0]["DataReady"]:
                LOGGER.error("Measurement timeout expired!", extra=extra)
                break

            # Проверка целостности данных
            elif not status[0]['CycleComplete'] or status[0]['DataCorrupt']:
                chrone.getFile()  # данные испорченные, но взять их нужно
                mess = f"Measurement with errors: " \
                       f"Status 'CycleComplete' = {status[0]['CycleComplete']}, " \
                       f"Status 'DataCorrupt' = {status[0]['DataCorrupt']}"
                LOGGER.warning(mess, extra=extra)
                continue

            # Считывание замера
            buffer = chrone.getFile()

            # Проверка размера и запись в хранилище
            if len(buffer) != 38528:
                dtime = datetime.now()
                path = f"measurements/{str(dtime).replace(':', '-')}_broke.txt"
                saveToFile(buffer, path)
                raise Exception(f"Measurement size is not correct! Came with size {len(buffer)}")

            # Проверка на нулевые Qm
            measurement = ChroneMeasurement(buffer)
            if not checkNullQm(measurement):
                attemptsQmCheck += 1
                if attemptsQmCheck > 2:
                    LOGGER.warning("Some Qm are zero, timeout expired!", extra=extra)
                else:
                    LOGGER.warning("Some Qm are zero, re-polling!", extra=extra)
                    continue

            # Усыпление платы
            LOGGER.info("The board falls asleep...", extra=extra)
            chrone.sleep()  # Плата может заснуть пропуская фазу измерения
            indicator = ""
            while perf_counter() - start < baseTime:
                status = chrone.getStatus()
                indicator = chrone.getIndicator()
                LOGGER.debug(f"Status: {status[1]}, Indicator: {indicator}", extra=extra)
                if status[0]["DataReady"]:  # ждём готовности замера
                    chrone.getFile()
                    sleep(15)
                elif indicator == "0x74":  # иногда срабатывает status[0]["DataCorrupt"]
                    LOGGER.info("The board fell asleep", extra=extra)
                    break
                else:
                    sleep(15)  # 15 секунд, время быстрого переопроса

            # Проверка, что плата спит
            if indicator != "0x74":
                LOGGER.error("The board didn't fall asleep!", extra=extra)

            break
        except Exception as ex:
            chrone.disconnect()
            LOGGER.critical(f"{ex}. Re-polling after 5 minutes", extra=extra)
            #break
            sleep(300)  # 5 минут, время среднего переопроса

    chrone.disconnect()
    LOGGER.info("Stopped polling the board", extra=extra)
    MODES[params.id] = "ping"

    return params, measurement


def pingThread(params: ChroneParams, pingTime: int):
    """Периодический опрос платы, чтоб не скучала"""

    chrone = ChroneControl(params.ip, params.port)
    extra = {"tag": params.name}

    while True:
        try:
            if MODES[params.id] == "ping":
                chrone.connect()
                status = chrone.getStatus()
                indicator = chrone.getIndicator()
                LOGGER.debug(f"PING, Status: {status[1]}, Indicator: {indicator}", extra=extra)
        except Exception as ex:
            LOGGER.critical(f"PING ERROR! {ex}", extra=extra)

        chrone.disconnect()
        sleep(pingTime)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def main():
    """Основной поток демона"""

    global logPath

    extra = {"tag": "Main"}

    LOGGER.info(f"Daemon start", extra=extra)

    try:
        user, pwd, = args.psql_user, args.psql_pwd
        base, host, port = args.psql_base, args.psql_host, args.psql_port
        postgres = PostgresControl(user, pwd, base, host, port)
        loggPostgres = PostgresControl(user, pwd, base, host, port)
    except Exception as ex:
        LOGGER.error(f"Error connecting to database. {ex}", extra=extra)

    # Считывание данных с базы
    postgres.connect()
    elements = postgres.getElements()
    connectionModbus = postgres.getConnectionModbus()
    postgres.disconnect()

    # Разворачивание Modbus TCP сервера
    modbus = ModbusServer(connectionModbus[0], connectionModbus[1])
    modbus.start()

    # Подключение сигнализации
    if args.alarm_port:
        alarmControl = AlarmControl(args.alarm_port, 9600)
        alarmControl.open()
        alarmControl.setAlarm(2, "0001")

    # Запуск ping-потоков
    for el in elements:
        #MODES[el.id] = 0
        MODES[el.id] = "start"
        ping = threading.Thread(target=pingThread, args=(el, 240), daemon=True)
        ping.start()

    # Цикл выполнения
    while True:

        # Обновление путей логов
        logPath = updatePath([LOGGER, MODBUS_LOGGER], logName, logPath)

        # Считывание данных с базы
        postgres.connect()
        elements = postgres.getElements()
        groups = postgres.getGroups()

        # Базовое время опроса, в секундах
        baseTime = max(600, postgres.getTime())
        start = perf_counter()

        # Запуск poll-потоков для считывания замеров с плат
        LOGGER.info("Polling the boards...", extra=extra)
        LOGGER.info(f"Poll frequency: {baseTime // 60} min, {baseTime % 60} sec", extra=extra)
        with ThreadPoolExecutor(2) as executor:
            futures = [executor.submit(pollThread, el, baseTime) for el in elements]
            #futures = [executor.submit(fakeThread, el, baseTime) for el in elements]
            records = [future.result() for future in futures]

        # Анализ замеров
        LOGGER.info("Measurement analysis...", extra=extra)
        severity = []
        for params, record in records:
            if record is not None:
                # Сохранение замеров
                LOGGER.info(f"Saving the measurement: {params.name}", extra=extra)
                # В базу
                try:
                    postgres.connect()
                    postgres.writeRecord(params.id, record)
                except Exception as ex:
                    LOGGER.critical(ex, extra=extra)
                # В modbus
                try:
                    data = record.getModbus([0, 0], groups)
                    #modbus.write(params.id * 2600, data)
                    modbus.write(0, data)
                except Exception as ex:
                    LOGGER.critical(ex, extra=extra)
                # В файл
                try:
                    path = f"measurements/{str(record.dtime).replace(':', '-')}.txt"
                    saveToFile(record.getRaw(), path)
                except Exception as ex:
                    LOGGER.critical(ex, extra=extra)

                # Проверка уставок
                severity.append(checkSeverityLvl(params, record))
                mess = f"{params.name}: [work: {severity[-1][3]}, " \
                       f"user: {severity[-1][1]}, first: {severity[-1][0]}, second: {severity[-1][2]}]"
                LOGGER.debug(mess, extra=extra)
            else:
                severity.append([0, 0, 0, 0])
                LOGGER.error(f"Failed to get the measurement: {params.name}", extra=extra)

        if args.alarm_port:
            alarm = computeAlarm(severity, half=False)
            mess = f"Alarm states set: [work: {alarm[3]}, " \
                   f"user: {alarm[1]}, first: {alarm[0]}, second: {alarm[2]}]"
            LOGGER.info(mess, extra=extra)
            alarmControl.setAlarm(2, alarm+alarm)

        #modbus.stop()
        #break

        # Переход в режим ожидания
        postgres.disconnect()
        timeleft = max(baseTime - (perf_counter() - start), 0)
        mess = f"The reading cycle is over, the transition to standby mode in: " \
               f"{round(timeleft) // 60} min, {round(timeleft) % 60} sec"
        LOGGER.info(mess, extra=extra)
        sleep(timeleft)


def start_servers():
    """Запуск эмулятора плат'"""

    s1 = ChroneServer("127.0.0.1", 1024)
    s2 = ChroneServer("127.0.0.1", 1025)
    s1.start()
    s2.start()


def is_running(name="chroneDemon.py") -> bool:
    """Поиск скрипта в активных процессах"""

    count = 0
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)
        except psutil.Error:
            continue
        if "python" in p.name() and len(p.cmdline()) > 1 and name in p.cmdline()[1]:
            count += 1
            if count > 1:
                print(p.cmdline())
                print("script already running!")
                return True

    return False


if __name__ == '__main__':
    if not is_running():
        if args.test:
            start_servers()
        main()

'''
    Базовый опрос:
        1 час

    Среднечастотный опрос:
        5 минут
        Время ожидания для переподключения к плате

    Частый опрос:
        15 секунд
        Время ожидания замера

    Если Qm равны нулю:
        1 раз - начать среднечастотный опрос
        2 раз - начать среднечастотный опрос
        3 раз - сохранить в базу, перейти к базовому опросу

    Фоновый опрос платы с периодичностью 4 мин 30 сек.
    Единственное действие, которое выполняет этот опрос,
     — это проверка статусов Python, что предотвращает перезагрузку Python.
    Напоминание: Python перезагружается, если не получает запросов в течение
     интервала времени *min(5 min, 3 * <время измерения>).*
'''