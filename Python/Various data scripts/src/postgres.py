# -*- coding: utf-8 -*-
"""
Функционал для взаимодействий с базой postgres

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- OUTER ----
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT

# ---- INNER ----


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

    # ---- CREATE запросы ----

    def createDB(self, dbName="Buffer"):
        """ """

        self.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = self.__connection.cursor()
        cursor.execute(f"CREATE DATABASE {dbName};")
        self.__connection.set_isolation_level(ISOLATION_LEVEL_DEFAULT)

    def dropDB(self, dbName="Buffer"):
        """ """

        self.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = self.__connection.cursor()
        cursor.execute(f"DROP DATABASE {dbName};")
        self.__connection.set_isolation_level(ISOLATION_LEVEL_DEFAULT)

    # ---- SELECT запросы ----

    def test(self, columns):
        """ """

        frames = {}

        for table, dtOrg, dtNeed, colOrg, colNeed, condition in columns:
            query = f'SELECT {dtOrg} AS {dtNeed}, {colOrg} AS {colNeed} ' \
                    f'FROM {table} {condition}'
            result = self.__execute(query, "all")

            frames[colNeed] = {dtNeed: [], colNeed: []}
            for dt, col in result:
                frames[colNeed][dtNeed].append(dt)
                frames[colNeed][colNeed].append(col)

        return frames

    # ---- INSERT запросы ----

    # def writeRecord(self, elid: int, record: ChroneMeasurement):
    #     """Запрос на добавление замера"""
    #
    #     lastid = self.__execute('SELECT max("Id") FROM "Values"')[0]
    #     lastid = lastid + 1 if lastid is not None else 1
    #
    #     query = 'INSERT INTO "Values" VALUES(%s, %s, %s, %s, %s, %s, %s)'
    #     params = (lastid, record.dtime, record.settings, record.ph_a, record.ph_b, record.ph_c, elid)
    #     self.__insert(query, params)


