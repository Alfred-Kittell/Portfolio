#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Реализация демона для периодического опроса прибора

(С) 2022 БО-Энерго, Альфред Дж. Киттелл
"""

# -- BUILT --
import argparse
from time import sleep, perf_counter

# -- OUTER --
import psutil

# -- INNER --
import bo_chrone.functions as bo_func
import bo_chrone.chroneData as bo_class
from bo_chrone.postgres import PostgresControl
from bo_chrone.chroneControl import ChroneControl
from bo_chrone.modbus import ModbusServer, AlarmControl, LOGGER as MODBUS_LOGGER

# -- COMMAND LINE --
parser = argparse.ArgumentParser()
parser.add_argument('--postgres_pwd', default='sa211222')
parser.add_argument('--postgres_user', default='postgres')
args = parser.parse_args()

###########################################################


def printHelp():
    """ """
    line = '\tHelp: \n' \
           '\t\t1 - h || help \n'\
           '\t\t9 - e || end'
    print(line)


def main():
    """ """

    # # Считывание данных с базы
    # postgres = PostgresControl(args.postgres_user, args.postgres_pwd, 'chrone')
    # postgres.connect()
    # elements = postgres.getElements()
    # groups = postgres.getGroups()
    # connectionModbus = postgres.getConnectionModbus()

    #
    while True:
        command = input('>> ')

        if command == '1' or command == 'h' or command == 'help':
            printHelp()
        elif command == '2' or command == 's' or command == 'status':
            ''
        elif command == '3' or command == 'e' or command == 'error':
            ''
        elif command == '4' or command == 'f' or command == 'file':
            ''
        elif command == '9' or command == 'x' or command == 'end':
            break



if __name__ == '__main__':
    main()
