# -*- coding: utf-8 -*-
"""

(С) 2025 БО-Энерго,
"""
# ---- BUILT ----
import os
import time
import math
import random
from datetime import datetime, timedelta

# ---- OUTER ----
#from numba import njit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from statsmodels.tsa.filters.hp_filter import hpfilter
from scipy.spatial import ConvexHull
from scipy.optimize import curve_fit

# ---- INNER ----
from src import functions as fun, names
from src.databankWalker import connect, get_data, get_datasets, get_dataset_id

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def combineData(root="", name='combine'):
    """Объединение файлов"""

    # временные константы
    dnames = {
        "час": 1/24,
        "30 минут": 1/48
    }

    root = r"data/combine"
    dateName = "datetime"
    name = "027-925"

    # Чтение файлов
    # frames = fun.get_data_from_files(root, names.columnFilter, names.columns_7hi)
    frames = fun.get_data_from_files(root, None, names.columns_7hi_v2, dateName)

    # Интерполяция с генерацией дат
    #dates = fun.dates_read(r"data/combine/date/1.xlsx")
    dates = fun.dates_generation(frames, dateName, 1/24/60)  # dnames["час"]
    frames = fun.frames_interpolation(frames, dates, dateName)

    # Исходные даты и значения
    #dates = fun.dates_combine(frames, dateName)
    #frames = fun.frames_combine(frames, dates, dateName)

    # Сглаживание всех полей
    df = pd.DataFrame(frames)
    # for frame in frames:
    #     cycle, frames[frame] = hpfilter(df[frame], 129600)
    #     df[frame] = frames[frame].round(3)

    # Сортировка полей
    print(f'\tSort cols ...')
    master_dict = names.create_master_dict()
    df = df[sorted(df.columns, key=lambda x: master_dict.get(x, len(master_dict)))]

    # запись
    print(f'Write to result/{name}.xlsx ...')
    #df = pd.DataFrame(frames)
    df.insert(0, dateName, dates)
    #df.to_csv(f"result/{name}.csv", encoding="utf-8", sep=';', index=False)
    df.to_excel(f"result/{name}.xlsx", index=False)
    print('Done')


def parse_7hi():
    """Парсер для файлов с расширением .7hi"""

    name = "Т-2 26196_history_2024_07_09_at_12_42_57"

    df1 = fun.parse_7hi(f"data/7hi/{name}.7hi", 1, names.columns_7hi_v1, "datetime")
    df1.to_excel(f"data/7hi/{name}.xlsx", index=False)

    # df2 = fun.parse_7hi('26197_history_2021_10_01_at_11_01_04.7hi', 1, test)
    # df2.to_excel("2021-10-01 at 11-01-04.xlsx")


def signals_parse():
    """ """

    n = 4

    dataPath = "data/signals/Чирк/4.csv"
    #dataPath = f"data/signals/from_dump/{n}.csv"
    dateName = "datetime"

    columns = {
        #"guid": 0,  # 0
        "datetime": 2,  # 2
        "signal": 0,  # 1
        "value": 1  # 3
    }
    guigs = fun.get_data_from_signals(dataPath, dateName, columns, n)

    for guig, frames in guigs.items():

        # Подмена на известное имя
        if guig in names.guids_equipment:
            guig = names.guids_equipment[guig]

        # Интерполяция с генерацией дат
        # dates = fun.dates_generation(frames, dateName, 1/48)  # 1/48
        # frames = fun.frames_interpolation(frames, dates, dateName)

        # Исходные даты и значения
        dates = fun.dates_combine(frames, dateName)
        frames = fun.frames_combine(frames, dates, dateName)

        print(f'Write - result/{guig}_new.xlsx ...')
        df = pd.DataFrame(frames)
        df.insert(0, dateName, dates)
        df.to_excel(f"result/{guig}_new.xlsx", index=False)


def postgres_parse():
    """Тест чтения бекапов"""

    dumpPath = "data/dumps/dump-postgres-202312011308_pahra"
    dateName = "datetime"

    # frames = fun.get_data_from_dump(names.columns_088)
    frames = fun.get_data_from_dump(names.columns_089)

    # Интерполяция с генерацией дат
    # dates = fun.dates_generation(frames, dateName, 1/24)  # 1/48
    # frames = fun.frames_interpolation(frames, dates, dateName)

    # Исходные даты и значения
    dates = fun.dates_combine(frames, dateName)
    frames = fun.frames_combine(frames, dates, dateName)

    # Сглаживание всех полей
    # for frame in frames:
    #     cycle, frames[frame] = hpfilter(frames[frame], 1600)
    #     frames[frame] = frames[frame].round(3)

    print('Write ...')
    df = pd.DataFrame(frames)
    df.insert(0, dateName, dates)
    # df.to_csv(f"088_1.csv", encoding="utf-8", sep=',', decimal=".", index=False)
    # df.to_csv(f"088_2.csv", encoding="utf-8", sep=';', decimal=",", index=False)
    # df.to_excel(f"result/087_interpolate.xlsx", index=False)
    df.to_excel(f"result/089_new.xlsx", index=False)


def recovery_excel():
    """
        Чистит эксель ужасно всратово качества:
        - Даты вместо значений
        - *** вместо пустых значений
        - числа записанные как текст
    """

    from dateutil.parser import parse

    def try_parse_float(value):
        try:
            return float(value.replace(',', '.'))
        except (ValueError, TypeError):
            return None

    def try_parse_datetime(value):
        try:
            return parse(value, dayfirst=True, fuzzy=True)
        except (ValueError, TypeError):
            return None

    df = pd.read_excel(f'data/exel/1.xlsx')
    cols = df.columns[1:]
    datacol = df.columns[0]
    result = {key: [] for key in df.columns}

    for ind in range(len(df)):
        result[datacol].append(df[datacol][ind])

        for col in cols:
            val = df[col][ind]

            # отсеиваем звёздочки
            if val == "***":
                val = None

            # отсеиваем строки
            elif isinstance(val, str):
                # отсеиваем числа записанные как текст
                buf_f = try_parse_float(val)
                buf_dt = try_parse_datetime(val)
                if buf_f:
                    val = buf_f
                # обрабатываем случаи с датами вместо чисел
                elif buf_dt:
                    # верифицированные данные есть, идём назад
                    if len(result[col]) and result[col][-1] is not None:
                        lastval = int(result[col][-1])

                        if buf_dt.day in [lastval, lastval+1, lastval-1]:
                            val = buf_dt.day
                        else:
                            print(f"херня какая-то [1] - {col}[{ind}] = {val} - [{lastval}]")
                            val = buf_dt.day
                    # верифицированных данных нет, идём вперёд
                    else:
                        found = False
                        for jnd in range(1, 20):
                            nextval = try_parse_float(df[col][ind+jnd])
                            if not nextval:
                                continue

                            found = True
                            if buf_dt.day == int(nextval):
                                val = buf_dt.day
                                break
                            else:
                                print(f"херня какая-то [2] - {col}[{ind}] = {val}")
                        if not found:
                            print(f"херня какая-то [3] - {col}[{ind}] = {val}")
                else:
                    print(f"херня какая-то [4] - {col}[{ind}] = {val}")

            # вносим итоговое значение
            result[col].append(val)

    df = pd.DataFrame(result)
    df.to_excel(f"result/recovery.xlsx", index=False)


def prof_test():
    """Проверка работоспособности для больших данных"""

    "ряд значений за 1 год для 1 сигнала 31536000 измерений"
    "каждое измерение (timestamp, value)"
    "Необходимо понять сколько памяти нужно для хранения таких данных для 10 сигналов"
    "Сколько времени потребуется для расчета среднего за ПОСЛЕДНИЕ 20 мин, 1 сутки, 1 месяц, 1 год"

    # Параметры
    seconds_per_year = 31_536_000
    seconds_20_min = 20 * 60
    seconds_1_day = 24 * 60 * 60
    seconds_1_month = 30 * seconds_1_day
    seconds_1_year = seconds_per_year

    # Сгенерируем данные за год
    values = np.random.rand(seconds_per_year).astype(np.float64)
    print(len(values))

    # Функция замера
    def benchmark_mean(name, window_size):
        subset = values[-window_size:]
        start = time.perf_counter()
        mean_val = np.mean(subset)
        duration = (time.perf_counter() - start) * 1_000  # в мс
        print(f"{name}: {window_size} точек | Среднее = {mean_val:.5f} | Время: {duration:.3f} мс")

    # Замеры
    benchmark_mean("20 минут", seconds_20_min)
    benchmark_mean("1 день", seconds_1_day)
    benchmark_mean("1 месяц", seconds_1_month)
    benchmark_mean("1 год", seconds_1_year)


def gen():
    """ """

    def generate_by_code(code: str) -> dict:
        gases = ["H2", "CH4", "C2H6", "C2H4", "C2H2"]
        result = {}

        # Значения по типу кода
        levels = {
            "А": lambda: round(random.uniform(1.05, 1.2), 3),
            "Б": lambda: round(random.uniform(1.0, 1.05), 3),
            "В": lambda: round(random.uniform(0.7, 0.99), 3),
            "Г": lambda: round(random.uniform(0.1, 0.6), 3)
        }

        for gas, letter in zip(gases, code.upper()):
            if letter not in levels:
                raise ValueError(f"Некорректный символ кода: {letter}")
            result[gas] = levels[letter]()

        return result

    def generate_valid_code() -> str:
        positions = list(range(5))
        code = ['Г'] * 5

        # Выбираем уникальную позицию для А
        a_pos = random.choice(positions)
        code[a_pos] = 'А'
        positions.remove(a_pos)

        # 50% шанс на Б
        if random.random() < 0.7:
            b_pos = random.choice(positions)
            code[b_pos] = 'Б'
            positions.remove(b_pos)

        # 50% шанс на В
        if random.random() < 0.7 and positions:
            v_pos = random.choice(positions)
            code[v_pos] = 'В'
            positions.remove(v_pos)

        return ''.join(code)

    def create_plot(code, point):
        """ """

        # Построим график как в методичке (по осям: газы vs относительные значения)
        gases = list(point.keys())
        values = list(point.values())

        plt.figure(figsize=(8, 5))
        plt.plot(gases, values, marker='o', linestyle='-', linewidth=2)
        plt.title(f"График состава газов для кода '{code}'")
        plt.ylabel("Относительная концентрация (ai)")
        plt.ylim(0, max(values) + 0.2)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Фиксированные кейсы
    samples = [
        "ВБАГГ",  # 1 - Термический дефект (до 300 ºС)
        "ГАВБГ",  # 2 - Термический дефект (от 300 до 700 ºС)
        "ГБВАГ",  # 3 - Термический дефект (более 700 ºС)
        "АВГГГ",  # 4 - ЧР
        "АВГГБ",  # 5 - Искровые разряды малой энергии
        "БВГГА",  # 6.1 - Дуга, искровые разряды большой энергии
        "ГВГБА",  # 6.2 - Дуга, искровые разряды большой энергии
        "ГБГВА",  # 7 - Композиция дефектов с преобладанием дефекта электрического характера
        "ВАБГГ",  # 8 - Композиция дефектов с преобладанием дефекта термического характера
    ]
    # Рандомные кейсы
    for i in range(41):
        samples.append(generate_valid_code())

    # Итоговые точки
    result = {"datetime": [],
              "H2": [], "CH4": [], "C2H6": [], "C2H4": [], "C2H2": [],
              "code": []}
    dt = datetime(2024, 12, 31, 23)
    for code in samples:
        for i in range(24):
            dt = dt + timedelta(hours=1)
            point = generate_by_code(code)
            result["datetime"].append(dt)
            result["H2"].append(point["H2"])
            result["CH4"].append(point["CH4"])
            result["C2H6"].append(point["C2H6"])
            result["C2H4"].append(point["C2H4"])
            result["C2H2"].append(point["C2H2"])
            result["code"].append(code)
    df = pd.DataFrame(result)
    df.to_excel("result/gen.xlsx")


def check_anom():
    """Проверка условий верификации"""

    def detect_anomalies_pd_v1(s: pd.Series):
        """
        s: pandas.Series with DatetimeIndex
        Returns: Series[bool] flags where True means anomaly
        """
        s = s.sort_index()
        # берёт разницу между соседними датами
        tau = s.index.to_series().diff().dt.total_seconds() / 86400.0  # days
        # считает относительное изменение (текущее - прошлое / прошлое)
        d1 = s.pct_change() * 100.0
        # считает допустимое отклонение
        delta = (1 + 20 / d1) * (50 * tau + 1)
        # проставляет флаг аномалии
        flags = (tau < 30) & (d1.abs() > delta)
        return flags.fillna(False), tau, d1, delta

    def detect_anomalies_pd_v2(s: pd.Series, freshness, roc_limit):
        """
        freshness - уставка по времени, в секундах
        roc_limit - уставка по значению
        """

        _tau = s.index.to_series().diff().dt.total_seconds()
        _d1 = s.diff().abs()
        flags = []

        # Первую считаем не аномальной
        flags.append(False)
        mark = 0
        # Обход точек
        for i in range(1, len(s)):
            tau = (s.index[i] - s.index[mark]).total_seconds()
            d1 = abs(s[i] - s[mark])
            if tau >= freshness or d1 < roc_limit:
                mark = i
                flags.append(False)
            else:
                flags.append(True)

        return pd.Series(flags), _tau, _d1

    p = [
        [60*10, 0.9],       # 1. ПС_Белый_Раст_АТ-5 - c_h2
        [60*60*4, 0.5],     # 2. ПС_Белый_Раст_АТ-5 - counter_overvoltage_total_year
        [60*10, 50]         # 3. ПС_Бескудниково_АТ-3 - i_hv_pa
    ]

    num = 3
    name = f"data/exel/anom_{num}.xlsx"
    df = pd.read_excel(name)
    df = df.dropna(subset=["datetime"]).set_index("datetime").sort_index()
    df = df[df.columns[0]]

    #flags, tau, d1, delta = detect_anomalies_pd_v1(df)
    flags, tau, d1 = detect_anomalies_pd_v2(df, p[num-1][0], p[num-1][1])
    result = {
        "datetime": df.index,
        "orig": df.values,
        "anom": np.where(flags.values, df.values, np.nan),
        "not anom": np.where(~flags.values, df.values, np.nan),
        "tau": tau,
        "d1": d1,
        #"delta": delta
    }

    plt.plot(result["datetime"], result["not anom"], '-o', label="не аномалия", color='g')
    plt.plot(result["datetime"], result["anom"], '-o', label="аномалия", color='r')
    plt.legend()
    plt.grid()
    plt.title("Бескудниково АТ-3 - i_hv_pa")
    plt.show()

    #df = pd.DataFrame(result)
    #df.to_excel(f"result/anom_{num}.xlsx", index=False)


def test_unic_fun():
    """ """

    def uniq_score(series, t):
        """ """

        try:
            series = np.asarray(series, dtype=float)
            series = series[np.isfinite(series)]

            if t == 1:  # старый
                n_total = len(series)
                n_unique = len(np.unique(series))
                return n_unique / n_total
            else:  # новый
                std = np.std(series)
                med = np.median(series)
                return std/med
        except:
            return None

    def uniq_score_2(series):
        series = np.array(series)
        n_total = len(series)
        n_unique = len(np.unique(series))

        # Поправка по равномерности распределения (энтропия)
        _, counts = np.unique(series, return_counts=True)
        probs = counts / n_total
        entropy = -np.sum(probs * np.log(probs)) / np.log(n_unique) if n_unique > 1 else 0

        return 100 * entropy

    def uniq_score_new(values, eps=None, weights=(0.5, 0.3, 0.2)):
        """
        Простая метрика "незалипания" сигнала без учёта времени.

        Компоненты:
          U — разнообразие (сколько уникальных клеток);
          E — равномерность распределения по клеткам (энтропия);
          S — живость (доля соседних шагов с изменением клетки).

        Итог: Score = 100 * (U^w1 * E^w2 * S^w3) * (1 - exp(-N/N0))

        Аргументы:
          values : iterable чисел (ряд)
          eps : шаг различения (если None — подберётся автоматически)
          weights : веса для (U, E, S)

        Возвращает:
          dict с полями score, U, E, S, eps, N
        """
        x = np.asarray(values, dtype=float)
        x = x[np.isfinite(x)]
        N = len(x)
        if N == 0:
            return 0

        # --- Авто-определение ε (шаг различения) ---
        if eps is None:
            diffs = np.diff(np.sort(x))
            diffs = diffs[diffs > 0]
            if len(diffs) > 0:
                step1 = np.median(np.percentile(diffs, np.linspace(0, 20, 21)))
                iqr = np.percentile(x, 95) - np.percentile(x, 5)
                step2 = 0.02 * iqr
                eps = max(step1, step2, 1e-9)
            else:
                eps = 1e-9

        # --- Квантуем значения в "клетки" ---
        bins = np.floor((x - x.min()) / eps).astype(int)
        uniq, counts = np.unique(bins, return_counts=True)
        D = len(uniq)

        # --- (1) Разнообразие (доля уникальных) ---
        U = 0.0 if N <= 1 else (D - 1) / (N - 1)

        # --- (2) Равномерность (энтропия) ---
        p = counts / counts.sum()
        if D > 1:
            H = -np.sum(p * np.log(p))
            Hmax = math.log(D)
            E = H / Hmax
        else:
            E = 0.0

        # --- (3) Живость (частота смен) ---
        if N > 1:
            switches = np.count_nonzero(bins[1:] != bins[:-1])
            S = switches / (N - 1)
        else:
            S = 0.0

        # --- Комбинированный скор ---
        wU, wE, wS = weights
        score_raw = (
                (U ** wU if U > 0 else 0.0)
                * (E ** wE if E > 0 else 0.0)
                * (S ** wS if S > 0 else 0.0)
        )
        score = 100 * score_raw

        res = {
            "score": float(score),
            "U": float(U),
            "E": float(E),
            "S": float(S),
            "eps": float(eps),
            "N": int(N),
        }
        print(res)

        return float(score)

    conn = connect()
    datasets = get_datasets(conn)
    result = {"хеш": [], "объект": [], "дисп. номер": [], "сигнал": [], "old": [], "new": []}
    i = 1

    for dataset in datasets:
        print(f"обрабатываю [{dataset[1]}] - {dataset[3]} - {dataset[2]}")
        data = get_data(conn, dataset[1])

        for col in data.columns:
            signal = data[col].dropna()
            score_old = np.round(uniq_score(signal.values, 1), 2) * 100
            score_new = np.round(uniq_score_2(signal.values), 2)
            result["хеш"].append(dataset[0])
            result["объект"].append(dataset[3])
            result["дисп. номер"].append(dataset[2])
            result["сигнал"].append(col)
            result["old"].append(score_old)
            result["new"].append(score_new)

            plt.plot(signal)
            plt.grid()
            plt.title(f"{dataset[0]} - {col} [{score_old}] [{score_new}]")
            plt.xticks(rotation=25, ha='right')
            plt.savefig(f"result/plots/{i} - {dataset[0]} - {col}.png")
            plt.close()
            i += 1

        df = pd.DataFrame(result)
        df.to_excel(f"result/uniq_test.xlsx", index=False)

    conn.close()

    #data = [5, 7]  # => ~0
    #data = [5, 5, 7, 5, 5, 5]  # => ~5..10
    #data = [1, 200, 30, 4, 5000]  # => ~100
    #data = [1, 1, 2, 2, 3, 3]  # => ~60
    #data = np.random.random(5)
    # score_1 = np.round(uniq_score_1(data), 2)
    # score_2 = np.round(uniq_score_2(data), 2)
    # score_new = np.round(uniq_score_new(data), 2)
    #
    # print(data)
    # print("Оценка 1: ", score_1)
    # print("Оценка 2: ", score_2)
    # print("Новая оценка: ", score_new)

    #plt.plot(data)
    #plt.title(f"{score_1}   {score_2}   {score_new}")
    #plt.show()


def test_speed():
    """Проверка гипотезы, что суточные скорости не нужны. Считает долю положительных"""

    root = r"data/exel/speed"
    result = {"hash": [], "object": [], "name": []}

    # взятие меты о датасетах
    conn = connect()
    datasets = get_datasets(conn)
    datasets = {item[0]: [item[3], item[2]] for item in datasets}

    for path in os.listdir(root):
        print(f"Read - {path}")
        hash = path.split(" - ")[0]
        obj, name = datasets[hash]
        result["hash"].append(hash)
        result["object"].append(obj)
        result["name"].append(name)
        current_len = len(result["hash"])

        df = pd.read_csv(os.path.join(root, path), sep=';', decimal=',')

        for col in df.columns:
            if "_roc_" in col:
                if col not in result:
                    result[col] = [None] * (current_len - 1)

                # фильтруем только реальную числовую часть
                filtered = df[col][(df[col] != 0) & (df[col].notna())]

                if filtered.empty:
                    val = None
                else:
                    val = np.round((filtered > 0).mean() * 100)
                result[col].append(val)

        # теперь нормализуем все существующие ключи
        for key in result:
            if key not in ["hash", "object", "name"]:
                # если длина меньше, значит для этого файла столбца не было
                if len(result[key]) < current_len:
                    result[key].append(None)

    # запись
    print(f'Write to result/speed.xlsx ...')
    df = pd.DataFrame(result)
    df.to_excel(f"result/speed.xlsx", index=False)
    print('Done')


def to_signal():
    """ """

    dataPath = "data/exel/с_roc.xlsx"
    df = pd.read_excel(dataPath)

    result = {"signal": [], "value": [], "timestamp": []}
    for col in df.columns[1:]:
        for i in range(len(df)):
            ts = df["timestamp"][i]
            val = df[col][i]
            if not pd.isna(val):
                result["signal"].append(col)
                result["value"].append(val)
                result["timestamp"].append(ts)
            else:
                t = 2

    print(f'Write - result/чирк.xlsx ...')
    df = pd.DataFrame(result)
    df.to_csv(f"result/чирк.csv", index=False)


def clean_asmd():
    """ """

    root = "data/exel/бэкап"
    #num = 0
    #files = os.listdir(root)
    #file = files[num]

    for file in os.listdir(root):
        if file.startswith('~'):
            continue

        path = os.path.join(root, file)
        print(f'Read {path} ...')
        df = pd.read_excel(path)

        # Переименовываем
        print(f'\tRename cols ...')
        rename_map = names.create_rename_map(df.columns)
        df = df.rename(columns=rename_map)
        # Сортируем
        print(f'\tSort cols ...')
        master_dict = names.create_master_dict()
        df = df[sorted(df.columns, key=lambda x: master_dict.get(x, len(master_dict)))]

        # Исправления времени
        print(f'\tCorrect cols ...')
        dt = pd.to_datetime(df["timestamp"], unit='s')
        df.insert(0, "datetime", dt)
        del df["timestamp"]
        # Исправления газов
        gases = [
            "h2",  # Водород
            "o2",  # Кислород
            "n2",  # Азот
            "co",  # Угарный газ
            "co2",  # Углекислый газ
            "ch4",  # Метан
            "c2h2",  # Ацетилен
            "c2h4",  # Этилен
            "c2h6",  # Этан
            "ch",  # Сумма углеводородных газов
            "tg",  # Сумма растворённых газов
            "tcg",  # Сумма горючих газов
            "thg",  # Сумма теплового газа
            "tdсg",  # Сумма горючих газов и CO
            "tcgh2",  # Сумма горючих газов и водорода
        ]
        correct_list = []
        for col in df.columns:
            for gas in gases:
                if gas in col and "_rel" not in col and col not in correct_list:
                    correct_list.append(col)
                    if "_roc" not in col:
                        df[col] = df[col].mask(df[col] < 0)
                    df[col] = df[col] * 10000

        # Сохраняем
        print(f'\tWrite - result/бэкап/{file} ...')
        df.to_excel(f"result/бэкап/{file}", index=False)


def r12_speed():
    """ """

    root = "data/exel/Отобранные"
    gases = [
        "h2",  # Водород
        "co",  # Угарный газ
        "co2",  # Углекислый газ
        "ch4",  # Метан
        "c2h2",  # Ацетилен
        "c2h4",  # Этилен
        "c2h6",  # Этан
    ]
    ddd = [
        ["day", 3600 * 24 * 1, 2, 1],
        ["week", 3600 * 24 * 7, 10, 7],
        ["month", 3600 * 24 * 30, 10, 30],
    ]

    for file in os.listdir(root):
        if file.startswith('~'):
            continue

        path = os.path.join(root, file)
        print(f'Read {path} ...')
        df = pd.read_excel(path)
        df['timestamp'] = (df['datetime'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

        result = {"datetime": df["datetime"].values}
        for ord in ["comm", "short"]:
            for rel in ["rel", "abs"]:
                for dt in ["day", "week", "month"]:
                    for gas in gases:
                        result[f"c_roc_{rel}_{gas}_{dt}_{ord}"] = []

        # Даты не фиксированные с произвольным шагом
        for gas in gases:
            print(f"\t - {gas}")
            for d, sec, min_point, f in ddd:
                for endDate in df["timestamp"].values:
                    startDate = endDate - sec
                    _df = df.loc[df["timestamp"].between(startDate, endDate)]
                    dt = list(_df["timestamp"] / (3600 * 24))
                    p = list(_df[f"c_{gas}"])

                    if len(_df) > min_point:
                        # Обычный
                        coef = np.polyfit(dt, p, 1)
                        c0 = np.average(_df[f"c_{gas}"])
                        c1 = coef[0] * dt[-1] + coef[1]
                        result[f"c_roc_abs_{gas}_{d}_comm"].append(coef[0])
                        if c0 > 1:
                            result[f"c_roc_rel_{gas}_{d}_comm"].append(((c1 - c0) / c0) * 100)
                        else:
                            result[f"c_roc_rel_{gas}_{d}_comm"].append(0)

                        # Сокращённый
                        #abs_v = (p[-1] - p[0]) / (dt[-1] - dt[0])
                        abs_v = (p[-1] - p[0]) / f
                        result[f"c_roc_abs_{gas}_{d}_short"].append(abs_v)
                        if p[0] > 0:
                            rel_v = ((p[-1] - p[0]) / p[0]) * 100
                            result[f"c_roc_rel_{gas}_{d}_short"].append(rel_v)
                        else:
                            result[f"c_roc_rel_{gas}_{d}_short"].append(0)

                        # контроль
                        # if abs(((c1 - c0)/c0)*100) > 3000:
                        #     print(c0, c1, coef[0], ((c1 - c0)/c0)*100)
                        #     plt.plot(dt, p, label="оригинальные")
                        #     plt.plot([dt[0], dt[-1]], [c0, c1], label="тренд")
                        #     plt.legend()
                        #     plt.grid()
                        #     plt.show()



                    else:
                        result[f"c_roc_abs_{gas}_{d}_comm"].append(0)
                        result[f"c_roc_rel_{gas}_{d}_comm"].append(0)
                        result[f"c_roc_abs_{gas}_{d}_short"].append(0)
                        result[f"c_roc_rel_{gas}_{d}_short"].append(0)

        # Сохраняем
        print(f'Write to result/c_roc.xlsx ...')
        df = pd.DataFrame(result)
        print(f'\tWrite - result/скорости/{file} ...')
        df.to_excel(f"result/скорости/{file}", index=False)


def r13():
    """ """

    def r13_aggregation(t, pressure):
        """Определение агрегатного состояния элегаза, жидкое/газовое"""

        # Полином 3 степени
        p = 0.000017908 * t ** 3 + 0.0036002511 * t ** 2 + 0.3377162034 * t + 12.6377890704
        # Экспонента
        # p = 11.2807155743 * np.exp(0.0286085818*t)

        if pressure > p:
            return "жидкое"  # подставить нужное
        else:
            return "газообразное"  # подставить нужное

    def r13_temperature_reserve(t, pressure):
        """Расчёт запаса по температуре конденсации элегаза"""

        # Поиск пересечения между полиномом и точкой при статичном давлении
        coeffs = [0.000017908, 0.0036002511, 0.3377162034, 12.6377890704 - pressure]
        roots = np.roots(coeffs)
        real_x = roots[np.isreal(roots)].real[0]  # температура в пересечении

        return t - real_x

    print(r13_aggregation(20, 10))  # газообразное
    print(r13_aggregation(20, 25))  # жидкое

    print(r13_temperature_reserve(20, 10))  # газообразное -> жидкое (28.5)
    print(r13_temperature_reserve(20, 25))  # жидкое -> газообразное (-7.4)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def calc_wcp(t, wcl):
    """Расчёт абсолютной влажности бумаги (по равновесным кривым)"""

    A = [5.55201183628544, 3.550143363628681, 2.6124613519000515]
    D = [-9.241908539822525, -5.250873492708096, -1.1645318138407346]
    F = [118.01981471458994, 106.5273381544408, 149.3079002660737]
    T = [283.610016850824, 270.41137812081746, 351.759407577563]

    return np.exp(D[0] + A[0] * np.sin(2 * np.pi * t / T[0] + 2 * np.pi / T[0] * F[0])) * wcl ** 3 - \
           np.exp(D[1] + A[1] * np.sin(2 * np.pi * t / T[1] + 2 * np.pi / T[1] * F[1])) * wcl ** 2 + \
           np.exp(D[2] + A[2] * np.sin(2 * np.pi * t / T[2] + 2 * np.pi / T[2] * F[2])) * wcl


def calc_wcl(t, wcp):
    """Расчёт кривых Ройзмана"""

    a = 1.21801 * wcp - 0.12651
    b = -0.00055 * wcp ** 2 + 0.00592 * wcp + 0.03562

    return a * np.exp(b * t)


def calc_rs(t, k):
    """Расчёт касательной rs"""

    return k * np.power(10, 7.23 - 1640 / (t + 273.15))


def find_max_dif(t, wcl):
    """Поиск максимальной разницы в wcl при одинаковой температуре"""

    df = pd.DataFrame({"t": t, "wcl": wcl})
    df["t"] = df["t"].round()
    max_dif = 0
    max_t = 0
    for un_t in df["t"].unique():
        vals = df["wcl"][df["t"] == un_t]
        dif = vals.max() - vals.min()
        if dif > max_dif:
            max_dif = dif
            max_t = un_t

    return max_dif, max_t


def calc_exp_tangent_min(t, wcl, f, wcp_lo=0.1, wcp_hi=30.0, iters=80):
    """
    Вычисляет минимальный wcp для экспоненциальной касательной к облаку точек (x, y > 0)
    Касательная проходит через ровно одну точку и огибает облако точек снизу
    wcp ищется с помощью бинарного приближения и необязательно входит в облако точек
    """

    # фильтр точек (на всякий, можно удалить в теории если данные нормальные)
    t = np.asarray(t, dtype=float)
    wcl = np.asarray(wcl, dtype=float)
    m = np.isfinite(t) & np.isfinite(wcl)
    t, wcl = t[m], wcl[m]
    if t.size == 0:
       raise ValueError("Нет валидных точек после фильтрации NaN/inf.")

    # вычисление wcp
    lo, hi = wcp_lo, wcp_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if np.max(f(t, mid) - wcl) <= 0:
            lo = mid
        else:
            hi = mid

    return lo


def calc_exp_tangent_max(t, wcl, f, wcp_lo=0.1, wcp_hi=20.0, iters=80):
    """
    Вычисляет максимальный wcp для экспоненциальной касательной к облаку точек (x, y > 0)
    Касательная проходит через ровно одну точку и огибает облако точек сверху
    wcp ищется с помощью бинарного приближения и необязательно входит в облако точек
    """

    # фильтр точек (на всякий, можно удалить в теории если данные нормальные)
    t = np.asarray(t, dtype=float)
    wcl = np.asarray(wcl, dtype=float)
    m = np.isfinite(t) & np.isfinite(wcl)
    t, wcl = t[m], wcl[m]
    if t.size == 0:
       raise ValueError("Нет валидных точек после фильтрации NaN/inf.")

    # вычисление wcp
    lo, hi = wcp_lo, wcp_hi
    for _ in range(iters):
        mid = (lo + hi) / 2
        if np.max(wcl - f(t, mid)) <= 0:
            hi = mid
        else:
            lo = mid

    return hi


def rozman():
    """ """

    t = np.arange(0.0, 110.1, 0.1)
    result = {"t": np.arange(0.0, 110.1, 0.1)}
    df = pd.read_excel("data/exel/wcp.xlsx")

    # Кривые Ройзмана
    #wcp = np.arange(0.1, 5.1, 0.1)  # [1, 2, 4]
    #for i in wcp:
    #    i = np.round(i, 1)
    #    result[f"wcl_{i}"] = []
    #    for j in t:
    #        result[f"wcl_{i}"].append(calc_wcl(j, i))

    max_wcl, max_t = find_max_dif(df["t_tp"], df["wcl_calc"])

    # Касательные
    tang_min = calc_exp_tangent_min(df["t_tp"], df["wcl_calc"], calc_wcl)
    tang_max = calc_exp_tangent_max(df["t_tp"], df["wcl_calc"], calc_wcl)
    print(f"wcp нижней касательной: {tang_min}")
    print(f"wcp верхней касательной: {tang_max}")
    result["tang_min"] = []
    result["tang_max"] = []
    for j in t:
        result["tang_min"].append(calc_wcl(j, tang_min))
        result["tang_max"].append(calc_wcl(j, tang_max))

    # rs
    result[f"rs"] = []
    result[f"rs_100"] = []
    # k = 1  # 100%
    k = calc_exp_tangent_max(df["t_tp"], df["wcl_calc"], calc_rs)  # wcl, t - точка верхней касательной
    print(f"rs верхней касательной: {k*100}")
    print(f"rs запас диэлектрической прочности: {100 - (k*100)}")
    for j in t:
        result[f"rs"].append(k * np.power(10, 7.23 - 1640 / (j + 273.15)))
        result[f"rs_100"].append(np.power(10, 7.23 - 1640 / (j + 273.15)))  # 100%

    print(f'Write to result/wcl_test.xlsx ...')
    df = pd.DataFrame(result)
    df.to_excel(f"result/wcl_test.xlsx", index=False)
    print('Done')


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def granger_causality():
    """Прогон дататестов на причинность на Грейнджер"""

    from statsmodels.tsa.stattools import grangercausalitytests

    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)  # шоб не спамил паскуда

    root = "data/exel/test"
    #root = "data/exel/influence"
    max_lag = 150
    result = {"hash": [], "object": [], "name": [], "Y": [], "X": [], "mode": []}
    #result.update({f"lag_{i}_p": [] for i in range(1, max_lag+1)})
    result.update({f"lag_0_{i}_p": [] for i in range(1, max_lag+1)})
    result.update({f"lag_1_{i}_p": [] for i in range(1, max_lag+1)})
    result.update({f"lag_2_{i}_p": [] for i in range(1, max_lag+1)})
    result.update({f"lag_3_{i}_p": [] for i in range(1, max_lag+1)})

    for file in os.listdir(root):
        if file.startswith("~$"):
            continue

        path = os.path.join(root, file)
        print(f"read - {path}")
        df = pd.read_excel(path)

        A1 = [item for item in df.columns[1:] if item.startswith("Y")]  # Y - на кого влияет
        A2 = [item for item in df.columns[1:] if not item.startswith("Y")]  # X - кто влияет

        for a1 in A1:
            for a2 in A2:
                # X - Y
                print(f"\tpair: {a1} - {a2}")
                if file.count(" - ") >= 2:
                    result["hash"].append(file.split(" - ")[0])
                    result["object"].append(file.split(" - ")[1])
                    result["name"].append(file.split(" - ")[2][:-5])
                else:
                    result["hash"].append("")
                    result["object"].append(file.split(" - ")[0])
                    result["name"].append(file.split(" - ")[1][:-5])

                result["mode"].append("Y-X")
                result["Y"].append(a1)
                result["X"].append(a2)

                data = df[[a1, a2]]
                #data = (data - data.min()) / (data.max() - data.min())  # минмакс
                #data = df[[a1, a2]].diff().iloc[1:]  # разности
                gc_res = grangercausalitytests(data, max_lag, verbose=False)
                #gc_res = grangercausalitytests(data, max_lag)

                for lag in gc_res:
                    #pval = np.round(gc_res[lag][0]["ssr_ftest"][1] * 100, 5)
                    #result[f"lag_{lag}_p"].append(pval)
                    result[f"lag_0_{lag}_p"].append(np.round(gc_res[lag][0]["ssr_ftest"][1] * 100, 5))
                    result[f"lag_1_{lag}_p"].append(np.round(gc_res[lag][0]["ssr_chi2test"][1] * 100, 5))
                    result[f"lag_2_{lag}_p"].append(np.round(gc_res[lag][0]["lrtest"][1] * 100, 5))
                    result[f"lag_3_{lag}_p"].append(np.round(gc_res[lag][0]["params_ftest"][1] * 100, 5))

                # X - Y
                #print(f"\tpair: {a2} - {a1}")
                # if file.count(" - ") >= 2:
                #     result["hash"].append(file.split(" - ")[0])
                #     result["object"].append(file.split(" - ")[1])
                #     result["name"].append(file.split(" - ")[2][:-5])
                # else:
                #     result["hash"].append("")
                #     result["object"].append(file.split(" - ")[0])
                #     result["name"].append(file.split(" - ")[1][:-5])
                #
                # result["mode"].append("X-Y")
                # result["Y"].append(a2)
                # result["X"].append(a1)
                #
                # data = df[[a2, a1]]
                # #data = (data - data.min()) / (data.max() - data.min())  # минмакс
                # #aata = df[[a2, a1]].diff().iloc[1:]  # разности
                # gc_res = grangercausalitytests(data, max_lag, verbose=False)
                # #gc_res = grangercausalitytests(data, max_lag)
                #
                # for lag in gc_res:
                #     pval = np.round(gc_res[lag][0]["ssr_ftest"][1] * 100, 5)
                #     result[f"lag_{lag}_p"].append(pval)
                #     #result[f"lag_0_{lag}_p"].append(np.round(gc_res[lag][0]["ssr_ftest"][1] * 100, 5))
                #     #result[f"lag_1_{lag}_p"].append(np.round(gc_res[lag][0]["ssr_chi2test"][1] * 100, 5))
                #     #result[f"lag_2_{lag}_p"].append(np.round(gc_res[lag][0]["lrtest"][1] * 100, 5))
                #     #result[f"lag_3_{lag}_p"].append(np.round(gc_res[lag][0]["params_ftest"][1] * 100, 5))

    print(f"Write to result/granger.xlsx ...")
    df = pd.DataFrame(result)
    df.to_excel(f"result/granger.xlsx", index=False)
    print("Done")


def ccm_causality():
    """Прогон дататестов на причинность на Конвергентное перекрестное отображение"""

    from causal_ccm.causal_ccm import ccm

    root = "data/exel/influence"
    libs = range(10, 110, 10)
    result = {"hash": [], "object": [], "name": [], "Y": [], "X": [], "mode": []}
    result.update({f"L_{i}_rho": [] for i in libs})

    for file in os.listdir(root):
        if file.startswith("~$"):
            continue

        path = os.path.join(root, file)
        print(f"read - {path}")
        df = pd.read_excel(path)

        A1 = [item for item in df.columns[1:] if item.startswith("c_")]  # Y - на кого влияет
        A2 = [item for item in df.columns[1:] if not item.startswith("c_")]  # X - кто влияет

        for a1 in A1:
            for a2 in A2:
                data = df[[a1, a2]]
                data = (data - data.min()) / (data.max() - data.min())  # минмакс

                # X - Y
                if file.count(" - ") >= 2:
                    result["hash"].append(file.split(" - ")[0])
                    result["object"].append(file.split(" - ")[1])
                    result["name"].append(file.split(" - ")[2][:-5])
                else:
                    result["hash"].append("")
                    result["object"].append(file.split(" - ")[0])
                    result["name"].append(file.split(" - ")[1][:-5])

                result["mode"].append("Y-X")
                result["Y"].append(a1)
                result["X"].append(a2)

                for lib in libs:
                    L = int(np.round(len(data) * lib/100, 0))
                    rho_df = ccm(data[a1], data[a2], L=L)
                    rho = np.max([0, rho_df.causality()[0]]) * 100
                    result[f"L_{lib}_rho"].append(rho)

                # X - Y
                if file.count(" - ") >= 2:
                    result["hash"].append(file.split(" - ")[0])
                    result["object"].append(file.split(" - ")[1])
                    result["name"].append(file.split(" - ")[2][:-5])
                else:
                    result["hash"].append("")
                    result["object"].append(file.split(" - ")[0])
                    result["name"].append(file.split(" - ")[1][:-5])

                result["mode"].append("X-Y")
                result["Y"].append(a2)
                result["X"].append(a1)

                for lib in libs:
                    L = int(np.round(len(data) * lib / 100, 0))
                    rho_df = ccm(data[a2], data[a1], L=L)
                    rho = np.max([0, rho_df.causality()[0]]) * 100
                    result[f"L_{lib}_rho"].append(rho)

    print(f"Write to result/convergent.xlsx ...")
    df = pd.DataFrame(result)
    df.to_excel(f"result/convergent.xlsx", index=False)
    print("Done")


def model(T, a, b, c):
    """Аппроксимация для L(T) = a * e^bT + c (x = T)"""

    return a * np.exp(b * T) + c


def approximator(func, X, Y, p0=None, bounds=None):
    """Аппроксиматор точек функцией"""

    #p0 = (1.0, 0.01, 0.0)  # начальные приближения (важно!)
    params, cov = curve_fit(func, X, Y, p0=p0, bounds=bounds)
    # cov - ковариационная матрица (если вдруг понадобится ошибка)

    return params


def ostwald():
    """Аппроксимация коэффициентов Оствальда"""

    exps = {
        "k": [30, 40, 50, 60, 70],
        "h2": [0.05198, 0.05400, 0.05994, 0.06507, 0.07102],
        "co": [0.1141, 0.1158, 0.1186, 0.1241, 0.1277],
        "co2": [0.4309, 0.3946, 0.3763, 0.3582, 0.3488],
        "ch4": [0.4309, 0.3946, 0.3763, 0.3582, 0.3488],
        "c2h2": [1.19, 1.09, 0.74, 0.53, 0.08],
        "c2h4": [1.19, 1.09, 0.74, 0.53, 0.08],
        "c2h6": [3.76, 3.31, 2.70, 2.01, 1.80],
    }
    sims = {
        "k": [303.0, 312.9, 323.0, 333.1, 343.1],
        "h2": [0.05390, 0.05596, 0.05700, 0.06000, 0.06500],
        "co": [0.1077, 0.1113, 0.1122, 0.1159, 0.1231],
        "co2": [0.4309, 0.3946, 0.3763, 0.3582, 0.3488],
        "ch4": [0.4055, 0.3991, 0.3774, 0.3702, 0.3635],
        "c2h2": [1.18, 1.09, 0.84, 0.67, 0.49],
        "c2h4": [1.18, 1.09, 0.84, 0.67, 0.49],
        "c2h6": [2.98, 2.78, 2.42, 2.03, 1.92],
    }

    # result = {"g": [], "a": [], "b": [], "c": []}

    # for g in exps:
    #     if g == "k":
    #         continue
    #     X = exps["k"]
    #     Y = exps[g]
    #     p0 = (0.01, 0.01, 0)
    #     a, b, c = approximator(model, X, Y, p0)
    #     result["g"].append(g)
    #     result["a"].append(a)
    #     result["b"].append(b)
    #     result["c"].append(c)

    # print(f"Write to result/ostwald.xlsx ...")
    # df = pd.DataFrame(result)
    # df.to_excel(f"result/ostwald.xlsx", index=False)
    # print("Done")

    X = exps["k"]
    Y = exps["c2h2"]
    p0 = (0.05, -0.01, 0.05)  # (0.01, 0.01, 0)
    bounds = (
        (0, -np.inf, 0),
        (np.inf, 0, np.inf))
    print(f"{approximator(model, X, Y, p0, bounds)}".replace('.', ','))


def ostwald_param():
    """аппроксимация параметров оствальда"""

    path = "data/exel/ostwald v3_.xlsx"
    df = pd.read_excel(path)
    name = df.columns[0]
    n_bins = 300

    fig, axs = plt.subplots(tight_layout=True)
    N, bins, patches = axs.hist(df[name], bins=n_bins)
    fracs = N / N.max()
    norm = colors.Normalize(fracs.min(), fracs.max())
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    #plt.hist(df[name])
    plt.xticks(np.arange(-10, 10+1, 10.0))
    plt.xlim([-10, 10])
    plt.grid(color='black')
    plt.show()


def dga_approx():
    """Аппроксимация кривых газов в DGA (соотношения)"""

    from scipy.interpolate import CubicSpline

    # данные
    data = pd.DataFrame({
        "c": [100, 150, 200, 275, 350, 450, 600, 800, 1000, 2000, 3000],
        "h2": [98, 90, 60, 15, 10, 12, 15, 15, 25, 45, 55],
        "c2h6": [1, 5, 25, 45, 40, 20, 10, 5, 2, 1, 0],
        "ch4": [1, 5, 15, 35, 45, 45, 35, 25, 15, 5, 1],
        "c2h4": [0, 0, 0, 5, 5, 22, 40, 55, 50, 15, 1],
        "c2h2": [0, 0, 0, 0, 0, 1, 0, 0, 8, 34, 43],
    })

    eps = 1e-6
    c = data["c"].values

    splines = {}

    for col in data.columns[1:]:
        y = np.log(data[col].values + eps)
        splines[col] = CubicSpline(c, y, bc_type='natural')

    def approx(c_new):
        result = {}
        for gas, spline in splines.items():
            result[gas] = np.exp(spline(c_new))
        return result

    result = {
        "c": [100, 150, 200, 275, 350, 450, 600, 800, 1000, 2000, 3000],
        "h2": [], "c2h6": [], "ch4": [], "c2h4": [], "c2h2": []}
    for c in result["c"]:
        a = approx(c)
        for g in approx(c):
            result[g].append(a[g])

    print(f'Write to result/dga_approx.xlsx ...')
    df = pd.DataFrame(result)
    df.to_excel(f"result/dga_approx.xlsx", index=False)
    print('Done')


def dga_mod():
    """Моделирование газов"""

    path = "data/exel/mod.xlsx"
    df = pd.read_excel(path)

    # константы
    v_oil = 10000
    v_gas = 1
    V_m = 24
    n0 = 0
    R = 8.314
    k_H = 50

    gases = ["h2", "ch4", "c2h6", "c2h4", "c2h2"]
    result = {}
    for g in gases:
        result[f"c_oil_gas_{g}_1"] = []
        result[f"c_oil_gas_{g}_2"] = []
        result[f"d_{g}"] = []

    for g in gases:
        for i in range(len(df)):
            L = df[f"L_{g}"][i]
            T = df[f"t"][i]
            c_def = df[f"c_def_{g}"][i]

            # решение
            A = v_gas / (k_H * L * R * T)
            B = v_oil / V_m
            C = -n0 - (v_oil / V_m) * c_def
            discriminant = (B ** 2) - 4 * A * C
            result[f"d_{g}"].append(discriminant)
            c1 = (-B + np.sqrt(discriminant)) / (2 * A)
            c2 = (-B - np.sqrt(discriminant)) / (2 * A)

            if discriminant < 0:
                c1 = None
                c2 = None
                #print("Нет вещественных решений")

            result[f"c_oil_gas_{g}_1"].append(c1)
            result[f"c_oil_gas_{g}_2"].append(c2)
            print(i)

    print(f'Write to result/dga_mod.xlsx ...')
    df = pd.DataFrame(result)
    df.to_excel(f"result/dga_mod.xlsx", index=False)
    print('Done')


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def sortcol():
    """"""

    dataPath = "result/combine.xlsx"
    save_name = "test.xlsx"
    df = pd.read_excel(dataPath)

    # Переименовываем
    print(f'Rename cols - {dataPath} ...')
    rename_map = names.create_rename_map(df.columns)
    df = df.rename(columns=rename_map)
    # Сортируем
    print(f'Sort cols - {dataPath} ...')
    master_dict = names.create_master_dict()
    df = df[sorted(df.columns, key=lambda x: master_dict.get(x, len(master_dict)))]

    # Сохраняем
    print(f'Write - result/{save_name} ...')
    df.to_excel(f"result/{save_name}", index=False)


def aggregation():
    """Агрегация датасетов по часам/дням"""

    path_file = "data/exel/043-411.xlsx"
    df = pd.read_excel(path_file)
    mode = 'H'  # 'D', 'W', 'M'

    # Устанавливаем дату индексом для ресемплинга
    df.set_index('datetime', inplace=True)
    # Агрегируем среднее по времени
    df = df.resample(mode).mean().reset_index()

    df.to_excel(f"result/aggre.xlsx", index=False)


def vectors():
    """Визуализация векторов НКВВ"""

    # Векторы (первые 3 — токи, последние 3 — напряжения)
    V1 = np.array([
        [52.317, 87.791],  # I ф A
        [51.945, -32.389],  # I ф B
        [51.817, -152.47],  # I ф C
        [290.199, 0],  # U ф A
        [291.255, -120.158],  # U ф B
        [289.887, 119.823],  # U ф C
    ])
    V2 = np.array([
        [52.317, 87.743],  # I ф A
        [51.699, -32.327],  # I ф B
        [51.488, -152.103],  # I ф C
        [290.308, 0],  # U ф A
        [291.251, -120.146],  # U ф B
        [289.944, 119.828],  # U ф C
    ])
    labels = ['I_ф_A', 'I_ф_B', 'I_ф_C', 'U_ф_A', 'U_ф_B', 'U_ф_C']
    colors = ['b', 'b', 'b', 'r', 'r', 'r']

    V = V2
    title = "АТ-2"

    # Добавляем тестовый вектор
    # labels.append('тест')
    # colors.append('g')
    #V = np.vstack([V, [10, 21.336]])


    # Приводим значения к координатам на графике
    for i in range(len(V)):
        amp = V[i][0]
        ang = V[i][1]
        V[i][0] = amp * np.cos((np.pi/180)*ang)  # X
        V[i][1] = amp * np.sin((np.pi/180)*ang)  # Y

    # Добавляем вектор небаланса
    labels.append('I_небаланс')
    colors.append('g')
    x = np.sum([V[0][0], V[1][0], V[2][0]])
    y = np.sum([V[0][1], V[1][1], V[2][1]])
    V = np.vstack([V, [x, y]])

    plt.figure(figsize=(10, 10))
    origin = np.zeros((2, V.shape[0]))
    plt.quiver(*origin, V[:, 0], V[:, 1], color=colors,
               scale=1, width=0.0035, angles='xy', scale_units='xy')

    # Радиус окружности (например, по модулю фазного напряжения)
    R = 290
    circle = plt.Circle((0, 0), R, color='gray', fill=False, linestyle='--', linewidth=1.2)
    plt.gca().add_patch(circle)

    # Добавим подписи на концах векторов
    for i in range(V.shape[0]):
        x, y = V[i]
        dx = 0.002 if x >= 0 else -0.04
        dy = 0.002 if y >= 0 else -0.01
        plt.text(x + dx, y + dy, labels[i], fontsize=14)

    # Украшаем
    plt.axhline(0, color='k', lw=1)
    plt.axvline(0, color='k', lw=1)
    plt.gca().set_aspect('equal')
    plt.grid(True)
    plt.xlim(-300, 300)
    plt.ylim(-300, 300)
    plt.tight_layout()
    plt.title(title)
    plt.show()


def correlations():
    """ """

    # df = pd.read_excel(f'data/exel/005-346.xlsx')
    # cols = df.columns[1:]
    # result = {"c": cols}
    #
    # for i in range(len(cols)):
    #     sel = cols[i]
    #     result[sel] = []
    #     for col in cols:
    #         cor = np.corrcoef(df[sel], df[col])[0][1]
    #         result[sel].append(cor)
    #
    # df2 = pd.DataFrame(result)
    # df2.to_excel("data/exel/corrtest.xlsx")

    df = pd.read_excel(f'data/exel/1.xlsx')
    print(df)


    #print(f"{l1} -> {l2} = {np.corrcoef(l1, l2)}")

    # print(f"c_ch4 -> i_pa_hv = {np.corrcoef(df1['c_ch4'], df1['i_pa_hv'])}")
    # print(f"c_ch4 -> i_pb_hv = {np.corrcoef(df1['c_ch4'], df1['i_pb_hv'])}")
    # print(f"c_ch4 -> i_pc_hv = {np.corrcoef(df1['c_ch4'], df1['i_pc_hv'])}")


def growthRate():
    """Расчёт скорости роста"""

    path = r'data/exel/dump.xlsx'
    df = pd.read_excel(path)

    gases = [
        "h2",  # Водород
        "co",  # Угарный газ
        "co2",  # Углекислый газ
        "ch4",  # Метан
        "c2h2",  # Ацетилен
        "c2h4",  # Этилен
        "c2h6",  # Этан
    ]
    result = {"timestamp": []}
    for dt in ["week", "month", "year"]:
        for gas in gases:
            result[f"c_roc_abs_{gas}_{dt}"] = []
            result[f"c_roc_rel_{gas}_{dt}"] = []

    ddd = [
        ["week", 3600*24*7, 10],
        ["month", 3600*24*30, 10],
        ["year", 3600*24*365, 50]]

    # Даты не фиксированные с произвольным шагом
    for gas in gases:
        print(gas)
        for d, sec, min_point in ddd:
            for endDate in df["timestamp"].values:
                startDate = endDate - sec
                _df = df.loc[df["timestamp"].between(startDate, endDate)]
                dt = list(_df["timestamp"] / (3600*24))
                p = list(_df[f"c_{gas}"])

                if len(_df) > min_point:
                    coef = np.polyfit(dt, p, 1)
                    #c0 = coef[0]*dt[0] + coef[1]
                    #c0 = p[0]
                    c0 = np.average(_df[f"c_{gas}"])
                    c1 = coef[0]*dt[-1] + coef[1]
                    result[f"c_roc_abs_{gas}_{d}"].append(coef[0])
                    if c0 > 1:
                        result[f"c_roc_rel_{gas}_{d}"].append(((c1 - c0)/c0)*100)
                    else:
                        #c0 = np.average(_df[f"c_{gas}"])
                        #result[f"c_roc_rel_{gas}_{d}"].append(((c1 - c0) / c0) * 100)
                        # for i in range(len(p)-1):
                        #     if p[i] > 1:
                        #         c0 = p[i]
                        #         result[f"c_roc_rel_{gas}_{d}"].append(((c1 - c0) / c0) * 100)
                        #         break
                        # if not c0 > 1:
                        result[f"c_roc_rel_{gas}_{d}"].append(0)

                    # контроль
                    # if abs(((c1 - c0)/c0)*100) > 3000:
                    #     print(c0, c1, coef[0], ((c1 - c0)/c0)*100)
                    #     plt.plot(dt, p, label="оригинальные")
                    #     plt.plot([dt[0], dt[-1]], [c0, c1], label="тренд")
                    #     plt.legend()
                    #     plt.grid()
                    #     plt.show()

                else:
                    result[f"c_roc_abs_{gas}_{d}"].append(0)
                    result[f"c_roc_rel_{gas}_{d}"].append(0)

    result["timestamp"] = df["timestamp"].values
    print(f'Write to result/c_roc.xlsx ...')
    df = pd.DataFrame(result)
    df.to_excel(f"result/с_roc.xlsx", index=False)


def add_anomaly():
    """Добавление двух типов перенапряжений"""

    root = "data/exel"
    name = "data4.xlsx"

    path = os.path.join(root, name)
    df = pd.read_excel(path)

    cols = df.columns
    data = {col: [] for col in cols}
    data2 = {col: [] for col in cols}
    count = len(cols)

    # Добавление малых аномалий
    for line in df.values:
        # Запись текущей строки
        for i in range(count):
            data[cols[i]].append(line[i])

        if line[38] + line[41] + line[44] > 0:
            for n in range(5):
                data[cols[0]].append(data[cols[0]][-1]+600)
                for i in range(1, count):
                    # Офф данные
                    if "off" in cols[i]:
                        data[cols[i]].append(None)
                    # Аномалии
                    elif n in [1, 2, 3] and line[38] == 1 and cols[i] == "u_pab_hv":
                        data[cols[i]].append(line[i]*random.randint(110, 120) / 100)
                    elif n in [1, 2, 3] and line[41] == 1 and cols[i] == "u_pbc_hv":
                        data[cols[i]].append(line[i]*random.randint(110, 120) / 100)
                    elif n in [1, 2, 3] and line[44] == 1 and cols[i] == "u_pca_hv":
                        data[cols[i]].append(line[i]*random.randint(110, 120) / 100)
                    # Все остальные
                    else:
                        data[cols[i]].append(line[i])

    df = pd.DataFrame(data)

    # Добавление больших аномалий
    for line in df.values:
        # Запись текущей строки
        for i in range(count):
            data2[cols[i]].append(line[i])

        if line[39] + line[42] + line[45] > 0:
            for n in range(5):
                data2[cols[0]].append(data2[cols[0]][-1]+5)
                for i in range(1, count):
                    # Офф данные
                    if "off" in cols[i]:
                        data2[cols[i]].append(None)
                    # Аномалии
                    elif n in [1, 2, 3] and line[39] == 2 and cols[i] == "u_pab_hv":
                        data2[cols[i]].append(line[i]*random.randint(125, 135) / 100)
                    elif n in [1, 2, 3] and line[42] == 2 and cols[i] == "u_pbc_hv":
                        data2[cols[i]].append(line[i]*random.randint(125, 135) / 100)
                    elif n in [1, 2, 3] and line[45] == 2 and cols[i] == "u_pca_hv":
                        data2[cols[i]].append(line[i]*random.randint(125, 135) / 100)
                    # Все остальные
                    else:
                        data2[cols[i]].append(line[i])

    df = pd.DataFrame(data2)
    df.to_excel(f"result/dataT4.xlsx", index=False)
    print('Done')


def create_signals():
    """ """

    path = "data/exel/O2,N2.xlsx"
    savePath = f"result/signals.csv"
    asset = "ee037632-2067-48b5-b469-fc4ea7474c7e"

    data = pd.read_excel(path)

    with open(savePath, "w") as f:
        f.write('"asset";"signal";"value";"timestamp"\n')

        for col in data.columns:
            if col == "datetime":
                continue
            print(col)
            for ind in range(len(data)):
                value = data[col][ind]
                dt = data["datetime"][ind].value // 1_000_000_000
                #dt = data["datetime"][ind].to_timestamp()
                f.write(f'"{asset}";"{col}";{value};{dt}\n')


def name_to_hash():
    """"""

    def custom_hash(input_str):
        """Превращает строку в Хеш-сумму"""
        char_map = {
            **{str(i): i + 1 for i in range(10)},  # Цифры
            **{ch: i + 11 for i, ch in enumerate("-_.:/#@&!?")},  # Спецсимволы
            **{ch: i + 21 for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")},  # Английский
            **{ch: i + 47 for i, ch in enumerate("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")},  # Русский
        }
        hash_value = 0
        checksum = 0
        for i, char in enumerate(input_str.upper()):
            if char in char_map:
                char_code = char_map[char]
                # Берём код символа и умножаем на квадрат позиции
                hash_value += char_code * ((i + 1) ** 2)
                # Рассчитываем контрольную сумму
                checksum += char_code

        return hash_value + checksum % 97

    inputs = [
        "Serveron Demo 1",
        "Serveron Demo 2",
        "Serveron Demo 3",
        "Serveron Demo 4",
        "Serveron Demo 5",
        "Serveron Demo 6",
        "Serveron Demo 7",
        "Serveron Demo 8",
        "Serveron Demo 9",
        "Serveron Demo 10",
        "Serveron Demo 11",
        "МЭС Центра 1",
        "МЭС Центра 2",
        "МЭС Центра 3",
        "МЭС Центра 4",
        "МЭС Центра 5",
        "МЭС Центра 6",
        "МЭС Центра 7",
        "МЭС Центра 8",
        "МЭС Центра 9",
        "МЭС Центра 10",
        "МЭС Центра 11",
        "МЭС Центра 12",
        "Сибур - Нефтехим Т - 1",
        "Калиниская АЭС 1",
        "Калиниская АЭС 2",
        "ПС Берсеневская 1",
        "ПС Берсеневская 2",
        "Волжская ГЭС Т - 1",
        "Волжская ГЭС Т - 2",
        "Волжская ГЭС Т - 3",
        "Волжская ГЭС 4",
        "БАЭС 1",
        "БАЭС 2",
        "БАЭС 3",
        "БАЭС 4",
        "БАЭС 5",
        "Котловка 1",
        "Котловка 2",
        "Camlin Demo 1",
        "Пахра АТ - 1",
        "Пахра АТ - 2",
        "Бескудниково АТ - 1",
        "Бескудниково АТ - 2",
        "Бескудниково АТ - 3",
        "Бескудниково АТ - 4",
        "Бескудниково АТ - 5",
        "Бескудниково АТ - 6",
        "Бескудниково Т - 1",
        "Бескудниково Т - 2",
        "Бескудниково Т - 3",
        "Бескудниково Т - 4",
        "Западная АТ - 1",
        "Западная АТ - 2",
        "Западная Т - 1",
        "Западная Т - 2",
        "Очаково АТ - 1",
        "Очаково АТ - 2",
        "Очаково АТ - 3",
        "Очаково АТ - 4",
        "Очаково АТ - 5",
        "Очаково АТ - 6",
        "Очаково АТ - 7",
        "Очаково АТ - 10",
        "Очаково АТ - 11",
        "Очаково Т - 8",
        "Очаково Т - 9",
        "Очаково Т - 12",
        "Очаково Т - 13",
        "Очаково Р - 1",
        "Очаково Р - 2",
        "Чагино АТ - 3",
        "Чагино АТ - 4",
        "Чагино АТ - 5",
        "Чагино АТ - 6",
        "Помары АТ - 1, ф.A",
        "Старый Оскол АТ - 5",
        "Талашкино АТ - 1",
        "Талашкино АТ - 2",
        "Талашкино АТ - 3",
        "Талашкино АТ - 4",
        "Означенное 2АТ",
        "Чесноковская АТ - 1",
        "Чесноковская АТ - 2",
        "ПС Преображенская 1",
        "Афипская АТ - 1",
        "Афипская Т - 1",
        "Афипская Т - 2"
        "Стачка АТ - 2",
        "Пахра АТ - 1 2",
        "Пахра АТ - 2 2",
        "ТП Владимир Т - 1",
        "ТП Владимир Т - 2",
        "ТП Владимир Т - 3",
        "Тютчево АТ - 1",
        "Тютчево АТ - 2",
        "Тютчево Т - 3",
        "Тютчево Т - 4",
        "Борисово АТ - 2",
        "Облучье 2Т",
        "Крутое Т - 1",
        "Мурманская АТ - 1",
        "Петрозаводск УШР 330 ф.A",
        "Петрозаводск УШР 330 ф.B",
        "Петрозаводск УШР 330 ф.C",
        "Тихвин Литейный Р - 1 - 330",
        "Менделеевская АТ - 1",
        "Менделеевская АТ - 2",
        "Завод Ильич Т - 1Н",
        "Завод Ильич Т - 2Н",
        "Ухта Р - 1 - 220",
        "Ростовская АТГ - 1",
        "Торобаева АТ - 3",
        "Карачинская Т1",
        "Нов - Анжерская АТ - 1 ф.A",
        "ERG Т8",
        "Пахра Т - 5",
        "Пахра Т - 6",
        "Белый Раст Т - 6",
        "Белый Раст Т - 7",
        "Белый Раст АТ - 1",
        "Белый Раст АТ - 2",
        "Белый Раст АТ - 4",
        "Белый Раст АТ - 5",
    ]

    inputs = ["Билибинская - 1Т"]

    for name in inputs:
        hash_value = custom_hash(name)
        print(hash_value)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


if __name__ == '__main__':
    #dataSelector()

    # files = [
    #     #[r'data/Парковая аналитика/Западная/Т-1', 'Западная-Т-1'],
    # ]
    #
    # for item in files:
    #     combineData(item[0], item[1])

    combineData()
    #parse_7hi()
    #signals_parse()
    #postgres_parse()
    #recovery_excel()
    #prof_test()
    #gen()
    #check_anom()
    #test_unic_fun()
    #test_speed()
    #to_signal()
    #clean_asmd()
    #r12_speed()
    #r13()

    #rozman()

    #granger_causality()
    #ccm_causality()
    #ostwald()
    #ostwald_param()
    #dga_approx()
    #dga_mod()

    #sortcol()
    #aggregation()
    #vectors()
    #correlations()
    #growthRate()
    #add_anomaly()
    #create_signals()
    #name_to_hash()

    #print(calc_wcp(40, 19))
    #print(calc_wcp(60, 42))

# datetime.fromtimestamp(1723194000)
