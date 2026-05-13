# -*- coding: utf-8 -*-
"""
Функционал для взаимодействий с базой postgres

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
from datetime import datetime

# ---- OUTER ----
import psycopg2
from psycopg2 import Error

# ---- INNER ----
from bo_chrone.chroneData import ChroneParams, ChroneMeasurement, Groups

###########################################################


class PostgresControl:
    """Класс для взаимодействия с базой postgres"""

    def __init__(self, user, password, database, host="localhost", port=5432):
        """
        Инициализирует новый экземпляр класса PostgresControl

        Parameters
        ----------
        user: str
            Пользователь для подключения
        password: str
            Пароль для подключения
        database: str
            Имя базы
        host: str
            IP адрес базы
        port: str
            Порт для подключения
        database: str
            Имя базы
        """

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    def connect(self):
        """Открывает соединение с базой"""

        self.__connection = psycopg2.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             port=self.port,
                                             database=self.database)

    def disconnect(self):
        """Закрывает соединение с базой"""

        self.__connection.close()

    # ---- Внутренняя логика ----

    def __execute(self, query: str, mode='one') -> tuple:
        """Выполнение SELECT запроса"""""

        cursor = self.__connection.cursor()
        cursor.execute(query)
        if mode == 'one':
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        cursor.close()

        return result

    def __insert(self, query: str, params: tuple):
        """Выполнение INSERT запроса"""

        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        self.__connection.commit()
        cursor.close()

    # ---- SELECT запросы ----

    def getConnectionModbus(self) -> tuple:
        """Запрос на получение параметров подключения для сервера Modbus"""

        return self.__execute('SELECT ip, port FROM "ConnectionModbus"')

    def getGroups(self) -> Groups:
        """Запрос на получение параметров зон для сжатия PRPD"""

        query = 'SELECT gd."Zone" FROM "ConnectionModbus" cm ' \
                'JOIN "Groups" g ON cm."Group" = g."Id" ' \
                'JOIN "GroupData" gd ON gd."Group" = g."Id" ' \
                'ORDER BY gd."Id"'
        result = self.__execute(query, 'all')

        return Groups([zone[0] for zone in result])

    def getElements(self) -> list:
        """Запрос на получение параметров плат"""

        elementId = self.__execute('SELECT "Id" FROM "EquipmentElements"'
                                   'WHERE active is true', 'all')
        result = []
        for element in elementId:
            query = f'SELECT el."Id", el."Name", port, url ' \
                    f'FROM "EquipmentElements" el ' \
                    f'JOIN "ConnectionPython" py ON el."Setting" = py."Id" ' \
                    f'WHERE el."Id" = {element[0]}'
            mainParams = self.__execute(query)

            query = f'SELECT sp."FirstValue", sp."SecondValue", ml."Value", ml."Criterial" ' \
                    f'FROM "SeverityLevels" sl ' \
                    f'JOIN "EquipmentElements" el ON el."SeverityLevel" = sl."Id" ' \
                    f'JOIN "SetPoints" sp ON sl."SetPoint" = sp."Id" ' \
                    f'JOIN "ModeLevel" ml ON sl."ModeLevel" = ml."Id" ' \
                    f'WHERE el."Id" = {element[0]}'
            severityParams = self.__execute(query)

            result.append(ChroneParams(mainParams, severityParams))

        return result

    def getTime(self) -> int:
        """Запрос на получение времени опроса, секундах"""

        query = f'SELECT cp."Interval" * u."Facrot" FROM "ConnectionPython" cp ' \
                f'JOIN "Units" u ON cp."IntervalUnit" = u."Id" ' \
                f'WHERE cp."Id" = 1'

        return int(self.__execute(query)[0])

    # ---- INSERT запросы ----

    def writeRecord(self, elid: int, record: ChroneMeasurement, hum=None, temp=None):
        """Запрос на добавление замера"""

        lastid = self.__execute('SELECT max("Id") FROM "Values"')[0]
        lastid = lastid + 1 if lastid is not None else 1

        query = 'INSERT INTO "Values" VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = (lastid, record.dtime, record.settings, record.ph_a, record.ph_b, record.ph_c, elid,
                  hum, temp)
        self.__insert(query, params)
