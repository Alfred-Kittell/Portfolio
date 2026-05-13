# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки работы модуля вывода.

Вызывать скрипт необходимо из папки "Chrone Python".
С параметром -i, устанавливает заданную сигнализацию модулю вывода
    Например: "python3 alarm_test.py -i 0001" - должна загореться синяя лампочка
Без параметра -i, возвращает сигнализацию модулю вывода
    Например: "python3 alarm_test.py" - вернёт текущую сигнализацию

Расположение лампочек: красная (1000), желтая (0100), зелёная(0010), синяя (0001)

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import argparse
import logging
from time import sleep

# ---- INNER ----
from bo_chrone.logger import createLogger, MODBUS_LOGGER
from bo_chrone.alarm import AlarmControl

# Настройка параметров командной строки
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', type=int, default=2)
parser.add_argument('-p', '--port', type=str, default='/dev/ttyS4')
parser.add_argument('-i', '--input', type=str)
parser.add_argument('-t', '--test', action='store_true', default=False)
args = parser.parse_args()

# Параметры логов
logName = 'logs/alarm_test_log.txt'
createLogger(logName, logger=MODBUS_LOGGER, level=logging.DEBUG, tag='Modbus')

# ---------------------------------------------------------


def main():
    port = args.port
    alarm = AlarmControl(port, 9600)  # 38400
    alarm.open()

    if args.test:
        while True:
            alarm.setAlarm(args.address, "0001")
            print("Горит синяя")
            sleep(20)
            alarm.setAlarm(args.address, "0100")
            print("Горит зелёная")
            sleep(20)
            alarm.setAlarm(args.address, "1000")
            print("Горит желтая")
            sleep(20)
            alarm.setAlarm(args.address, "0010")
            print("Горит красная")
            sleep(20)
            break
    else:
        if args.input:
            alarm.setAlarm(args.address, args.input)
        else:
            MODBUS_LOGGER.info(alarm.getAlarm(args.address))

    alarm.close()


if __name__ == '__main__':
    main()
