# -*- coding: utf-8 -*-
"""

"""
# ---- BUILT ----
import os

# ---- OUTER ----
import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def get_datasets(conn) -> dict:
    """Получить информацию о датасетах"""
    with conn.cursor() as cur:
        cur.execute("SELECT d.hash_code, d.id, d.name, o.name "
                    "FROM datasets d JOIN objects o ON d.object_id = o.id "
                    "ORDER BY o.name, d.name, d.hash_code")
        result = cur.fetchall()
        return result if result else None


def get_data(conn, dataset_id=17):
    """Получить данные"""
    query = f"""
    SELECT
        sd.datetime,
        s.code AS signal_code,
        sd.value
    FROM signal_data sd
    JOIN signals s ON sd.signal_id = s.id
    JOIN groups g ON s.group_id = g.id
    WHERE g.code = 'gases'
      AND s.category = 'online'
      AND sd.dataset_id = {dataset_id}
    ORDER BY sd.datetime, s.code;
    """
    query = f"""
        SELECT
            sd.datetime,
            s.code AS signal_code,
            sd.value
        FROM signal_data sd
        JOIN signals s ON sd.signal_id = s.id
        JOIN groups g ON s.group_id = g.id
        WHERE sd.dataset_id = {dataset_id}
        ORDER BY sd.datetime, s.code;
        """
    df = pd.read_sql(query, conn)
    try:
        pivot = df.pivot(index='datetime', columns='signal_code', values='value')
    except Exception as ex:
        print(f"Проблема в [{dataset_id}]. {ex}")
    #pivot = df.pivot(index='datetime', columns='signal_code', values='value')
    pivot = df.pivot_table(index='datetime', columns='signal_code', values='value', aggfunc='mean')
    return pivot


def connect():
    """Подключение к банку"""

    conn = psycopg2.connect(
        dbname="data_bank",  # databank
        user="bo-energo",    # postgres
        password="passwordSTRONG",   # admin
        host="10.0.1.69",   # localhost
        port="5432"
    )

    return conn


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def get_dataset_id(conn, hash_code):
    """Ищет dataset_id по hash_code"""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM datasets WHERE hash_code = %s", (hash_code,))
        result = cur.fetchone()
        return result[0] if result else None


def get_signal_ids(conn, signal_names):
    """Находит signal_id для каждого сигнала по его имени"""
    signal_ids = {}
    with conn.cursor() as cur:
        for signal_name in signal_names:
            cur.execute("SELECT id FROM signals WHERE code = %s", (signal_name,))
            result = cur.fetchone()
            if result:
                signal_ids[signal_name] = result[0]
            else:
                print(f"\t - Сигнал '{signal_name}' не найден!")
    return signal_ids


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def find_datesets():
    """
    Рекурсивный поиск датасетов в виде экселек
    С приоритетом для префикса
    """

    # Путь к корневой папке
    root_folder = "data/databank"

    # Приоритеты для Excel-файлов (чем ниже число, тем выше приоритет)
    priorities = {"clean_all": 1, "_all": 2, "_onl": 3, "_off": 4, "_new": 5}

    # Словарь для хранения найденных файлов
    files_dict = {}

    # if not file.startswith("test") and not file.startswith("~$"):


    for root, dirs, files in os.walk(root_folder):
        # Фильтруем только Excel файлы
        excel_files = [f for f in files if f.endswith(".xlsx")]

        if not excel_files:
            continue

        # Создаём словарь для файлов в текущей папке
        files_by_prefix = {prefix: None for prefix in priorities}

        for file in excel_files:
            for prefix in priorities:
                if file.endswith(f"{prefix}.xlsx"):
                    files_by_prefix[prefix] = os.path.join(root, file)
                    break

        # Выбираем файл с максимальным приоритетом
        for prefix in priorities:
            if files_by_prefix[prefix]:
                folder_name = os.path.basename(root)
                files_dict[folder_name] = files_by_prefix[prefix]
                break

    return files_dict


def import_to_db(files_dict):
    """Заливка датасетов в базу"""

    # Настройки для подключения к базе
    conn = connect()

    # Обходим файлики
    print("Процесс заливки:")
    for folder_name, file_path in files_dict.items():
        file_name = os.path.basename(file_path)
        hash_code = file_name.split("_")[0]  # парсим хеш
        print(f"[{hash_code}]: {folder_name}\\{file_name}")

        # Находим dataset_id
        dataset_id = get_dataset_id(conn, hash_code)
        if dataset_id is None:
            print(f"\t - Датасет не найден!")
            continue

        # Читаем Excel файл
        df = pd.read_excel(file_path)
        df['datetime'] = pd.to_datetime(df['datetime'])

        # Находим signal_ids
        signal_names = df.columns[1:]
        signal_ids = get_signal_ids(conn, signal_names)

        # Подготовка данных для вставки
        data_to_insert = []
        for index, row in df.iterrows():
            datetime = row['datetime']
            for signal_name, value in row.items():
                if signal_name == 'datetime' or pd.isna(value):
                    continue  # Пропускаем пустые значения
                signal_id = signal_ids.get(signal_name)
                if signal_id:
                    data_to_insert.append((dataset_id, signal_id, datetime, value))

        if not data_to_insert:
            print("\t - Нет данных для вставки.")
            continue

        # continue  # без вставки

        # Вставка данных
        print("\t Заливка данных")
        limit = 100_000
        for i in range(0, len(data_to_insert), limit):
            if i > 0:
                print(f"\t - {round(i/len(data_to_insert)*100, 1)}%")
            with conn.cursor() as cur:
                insert_query = sql.SQL("""
                    INSERT INTO signal_data (dataset_id, signal_id, datetime, value)
                    VALUES %s
                    ON CONFLICT DO NOTHING;
                """)
                execute_values(cur, insert_query, data_to_insert[i:i + limit][i:i + limit])

            conn.commit()
        #break

    # Закрываем соединение
    conn.close()


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def main():
    """ """

    files_dict = find_datesets()
    import_to_db(files_dict)


if __name__ == '__main__':
    main()

