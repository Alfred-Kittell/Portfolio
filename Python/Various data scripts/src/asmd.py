# -*- coding: utf-8 -*-
"""Скрипт снятия данных с клика АСМД"""
# ---- BUILT ----
import os
from collections import defaultdict
from urllib.parse import urlparse
from pathlib import Path

# ---- OUTER ----
import clickhouse_driver
from clickhouse_driver import Client
import pandas as pd

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class ClickhouseControl:
    """Класс для взаимодействия с базой"""

    def __init__(self, user="default", password="", database="asmd_1", host='10.19.166.196', port=9000):
        """
        Инициализирует новый экземпляр класса ClickhouseControl

        Parameters
        ----------
        user: str
            Пользователь для подключения
        password: str
            Пароль для подключения
        database: str
            Имя базы
        host: str, optional
            IP адрес базы
        port: str, optional
            Порт для подключения
        """

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    @classmethod
    def from_url(cls):
        """
        Инициализирует новый экземпляр класса ClickhouseControl со строки URL.
        Формат ULR: clickhouse://DB_USER:PASSWORD@DB_HOST:PORT/DB_NAME
        """
        url = "clickhouse://default:@10.19.166.196:9000/asmd_1"
        params = urlparse(url)

        return cls(user=params.username,
                   password=params.password,
                   host=params.hostname,
                   port=params.port,
                   database=params.path[1:])

    def connect(self):
        """Открывает соединение с базой"""

        self.__connection = clickhouse_driver.Client(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database)
        try:
            self.__connection.connection.connect()
            return True
        except Exception as ex:
            print(f"Не удалось создать соединение с Clickhouse. {ex}")
            return False

    def disconnect(self):
        """Закрывает соединение с базой"""

        self.__connection.disconnect_connection()

    def get_connection(self) -> Client:
        """Возвращает экземпляр подключения к Clickhouse"""

        return self.__connection


def get_data(substation_name, asset_name, signals, date_range):
    query = f"""
        select substation, asset, signal_code, value, d.dt from (
        select d.name as substation, e.name as asset, guid_parameter as signal,s.code as signal_code, t.value_parameter as value, t.date as dt
        from asmd_1.parameter_value_meterpoint t 
        left join asmd_1.parameter_name_diagnostic s on t.guid_parameter::text=s.guid
        left join asmd_1.equipment e on t.guid_equipment::text=e.guid
        left join asmd_1.division d on d.guid=e."idSubstation"
        where date >= '{date_range[0]}' AND date < '{date_range[1]}'
        and d.name = '{substation_name}'
        and e.name='{asset_name}'
        and signal_code IN {signals}
         order by  1,2,3
        ) d
        order by  d.dt desc;
    """
    # where date between '{date_range[0]}' and '{date_range[1]}'


    click_manager: ClickhouseControl = ClickhouseControl.from_url()
    if not click_manager.connect():
        print("Unable to connect to Clickhouse")
        return {}

    conn: Client = click_manager.get_connection()

    data = defaultdict(dict)
    query_result = conn.execute(query)
    for item in query_result:
        timestamp = item[4]
        code = item[2]
        value = item[3]
        data[timestamp][code] = value
        data[timestamp]["timestamp"] = timestamp

    return list(sorted(data.values(), key=lambda x: x.get("timestamp")))


def save_to_excel(data, asset_name, date_range):

    print(f"{len(data)} rows")
    df = pd.DataFrame(data)
    filename = f"{asset_name}_{date_range[0]}_{date_range[1]}.xlsx"
    filename = filename.replace(" ", "_")
    df.to_excel(filename)
    print(f"Saved to {filename}")


def main():
    """"""

    # сбор метаданных
    signal_path = "сигналы.xlsx"
    meta = pd.read_excel(signal_path)
    meta = (
        meta.groupby(['substation', 'asset'])['signal_code']
        .apply(list)
        .unstack()  # Превращает второй уровень индекса (asset) в столбцы
        .apply(lambda x: x.dropna().to_dict(), axis=1)
        .to_dict()  # Делает substation ключами словаря
    )
    # даты взятия
    date_range = ('2025-01-01', '2026-02-01')
    periods = [
        (start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        for start, end in zip(
            pd.date_range(date_range[0], date_range[1], freq='MS'),
            pd.date_range(date_range[0], date_range[1], freq='M')
        )
    ]
    # путь сохранения
    root = Path("data")
    root.mkdir(parents=True, exist_ok=True)

    #if file_path.exists():
    #    print(f"Пропускаем {file_path}, уже скачано")
    #    continue

    # обход
    for sub in meta:
        print(f"{sub}:")
        for ass in meta[sub]:
            print(f"\t{ass}:")
            signals = meta[sub][ass]
            path = root / f"{sub} - {ass}"
            path.mkdir(parents=True, exist_ok=True)
            for date_range in periods:
                filepath = path / f"({date_range[0]}).xlsx"
                if filepath.exists():
                    if os.path.getsize(filepath) > 10000:
                        print(f"\t\t- {date_range[0]} - pass")
                        continue
                #data = get_data(sub, ass, signals, date_range)
                data = {}
                print(f"\t\t- {date_range[0]}")
                df = pd.DataFrame(data)
                df.to_excel(filepath)


if __name__ == "__main__":
    main()
