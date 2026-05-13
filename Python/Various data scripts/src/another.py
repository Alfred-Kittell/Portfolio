# -*- coding: utf-8 -*-

import os
import json
import random
from copy import copy
from itertools import *
from datetime import datetime, timedelta

#from numba import njit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter
from phik import phik_from_array as phk_from_arr
from scipy.optimize import minimize
import scipy.stats as sts

from src import functions as fun, names

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def ASMDAnalytics():
    """Аналитика АСМД"""

    path = "data/exel/1.1.xlsx"
    dt = pd.read_excel(path)

    data1 = [f"{item[0]}\n{item[1]}" for item in dt[["2а", "2б"]].values if item[0] == "МЭС Сибири"]
    data2 = [f"{item[0]}\n{item[1]}" for item in dt[["2а", "2б"]].values if item[0] == "МЭС Центра"]
    data3 = [f"{item[0]}\n{item[1]}" for item in dt[["2а", "2б"]].values if item[0] == "МЭС Юга"]

    labels1, counts1 = np.unique(data1, return_counts=True)
    labels2, counts2 = np.unique(data2, return_counts=True)
    labels3, counts3 = np.unique(data3, return_counts=True)

    plt.bar(labels1, counts1, align='center', label="МЭС Сибири")
    plt.bar(labels2, counts2, align='center', label="МЭС Центра")
    plt.bar(labels3, counts3, align='center', label="МЭС Юга")

    #plt.grid(which='major', color='#CCCCCC', linestyle='--')
    #plt.grid(which='minor', color='#CCCCCC', linestyle=':')
    plt.grid(axis="y")
    #plt.xticks(rotation=25)
    plt.legend()

    plt.show()

    t = 1


def correlations():
    """ """

    #df1 = pd.read_excel(f'data\\test\\210524 7X.xlsx')

    l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    l2 = [2, 2, 1, 4, 4, 4, 4, 1, 1, 1]
    print(f"{l1} -> {l2} = {phk_from_arr(l1, l2)}")
    print(f"{l1} -> {l2} = {np.corrcoef(l1, l2)}")

    # phk_restore = phk_from_arr(df1["c_ch4"], df1["i_pa_hv"], ['x', 'y'], 10)
    # print(f"c_ch4 -> i_pa_hv = {phk_from_arr(df1['c_ch4'], df1['i_pa_hv'])}")
    # print(f"c_ch4 -> i_pb_hv = {phk_from_arr(df1['c_ch4'], df1['i_pb_hv'])}")
    # print(f"c_ch4 -> i_pc_hv = {phk_from_arr(df1['c_ch4'], df1['i_pc_hv'])}")
    # print(f"i_pa_hv -> c_ch4 = {phk_from_arr(df1['i_pa_hv'], df1['c_ch4'])}")
    # print(f"i_pb_hv -> c_ch4 = {phk_from_arr(df1['i_pb_hv'], df1['c_ch4'])}")
    # print(f"i_pc_hv -> c_ch4 = {phk_from_arr(df1['i_pc_hv'], df1['c_ch4'])}")

    # print(f"c_ch4 -> i_pa_hv = {np.corrcoef(df1['c_ch4'], df1['i_pa_hv'])}")
    # print(f"c_ch4 -> i_pb_hv = {np.corrcoef(df1['c_ch4'], df1['i_pb_hv'])}")
    # print(f"c_ch4 -> i_pc_hv = {np.corrcoef(df1['c_ch4'], df1['i_pc_hv'])}")


def test_3D():
    """ """

    data = {"temp": [], "i": [],
            "c_h2": [], "c_co": [], "c_co2": [], "c_ch4": [], "c_c2h2": [], "c_c2h4": [], "c_c2h6": []}
    c_h2_base = 15.9
    c_co_base = 563.9
    c_co2_base = 7362.9
    c_ch4_base = 72.9
    c_c2h2_base = 1.1
    c_c2h4_base = 18.7
    c_c2h6_base = 16.9

    for i in range(22, 122, 10):
        for temp in range(38, 48):
            data["temp"].append(temp)
            data["i"].append(i)
            data["c_h2"].append(np.sin(temp/11+i/25)+c_h2_base + np.random.normal(0, 0.1))
            data["c_co"].append(np.sin(temp/5+i/40)+c_co_base + np.random.normal(0, 0.1))
            data["c_co2"].append(np.sin(temp/6+i/25)+c_co2_base + np.random.normal(0, 0.1))
            data["c_ch4"].append(np.sin(temp/20+i/50)+c_ch4_base + np.random.normal(0, 0.1))
            data["c_c2h2"].append(np.sin(temp/3+i/14)+c_c2h2_base + np.random.normal(0, 0.1))
            data["c_c2h4"].append(np.sin(temp/15+i/56)+c_c2h4_base + np.random.normal(0, 0.1))
            data["c_c2h6"].append(np.sin(temp/26+i/56)+c_c2h6_base + np.random.normal(0, 0.1))

    df = pd.DataFrame(data)
    #df.sort_values("i", inplace=True)
    #df.sort_values("temp", inplace=True)
    print(df)

    X, Y = np.meshgrid(df["temp"], df["i"])
    Z = np.sin(X/26+Y/56)+c_c2h6_base + np.random.normal(0, 0.1, 100)

    gas = "c_c2h6"

    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.set_title(gas)
    ax.set_xlabel('temp')
    ax.set_ylabel('i')
    #ax.set_zlabel(gas)

    #plt.show()
    df.to_excel(f"result/test.xlsx", index=False)


def mapping():
    """ """

    def obj_func(variable, val):
        D, A, Fi = variable
        T = 24
        result = np.sum(np.abs((D + A * np.sin((2 * np.pi / T) * np.arange(24) + Fi)) - val))

        return result

    df = pd.read_excel(f"data\\exel\\Weather and t_en 1h.xlsx", sheet_name="norm")

    bins = np.arange(-2, 12, 0.5)
    histData = {i: [] for i in range(24)}

    for ind in range(len(df)):
        dt = df["datetime"][ind]
        histData[dt.hour].append(df["Столбец1"][ind])

    # fig, ax = plt.subplots()
    # #ax.hist(df["Столбец1"], bins=bins)
    # ax.hist(histData[17], bins=bins)
    # ax.set_xticks(bins, minor=False)
    # ax.set_title("Разброс между показаниями датчика и температурой по погоде за 17 час")
    # ax.set_xticks(bins, minor=False)
    # ax.set_yticks(range(0, 16, 2), minor=False)
    # plt.grid("x")
    # plt.show()

    buf = {"hour": [], "mu": [], "sigma": []}

    #fig, ax = plt.subplots(6, 2, sharex='col', sharey='row')
    #fig, ax = plt.subplots(6)
    fig, ax = plt.subplots()
    for hour, data in histData.items():
        #if hour < 0 or hour < 5:
        #if hour > 5:
        #if hour < 12 or hour > 17:
        #if hour < 18:
        #    continue
        #x = hour % 6

        # Аппроксимация
        mu = np.mean(data)
        sigma = np.std(data)
        scale = 40
        y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2)) * scale
        buf["hour"].append(hour)
        buf["mu"].append(mu)
        buf["sigma"].append(sigma)

        # График
        # ax[x].hist(data, bins=bins, label=f"за {hour} час")
        # ax[x].plot(bins, y, '--', color='black', label=f"Аппроксимация,"
        #                                                f" μ={mu: .2f}, σ={sigma:.2f}")
        # ax[x].set_xticks(bins, minor=False)
        # ax[x].set_yticks(range(0, 16, 2), minor=False)
        # #ax[x, y].set_title(f"Разброс между показаниями датчика и температурой по погоде, "
        # #             f"за {hour} час")
        # #ax[x, y].set_title(f"за {hour} час")
        # ax[x].grid("x")
        # ax[x].legend()
        # #plt.tight_layout()
        # #fig.set_size_inches(10, 3)
        # #plt.savefig(f"{hour}.png")
    # fig.suptitle("Разброс между показаниями датчика и температурой по погоде по часам")
    # plt.show()

    # Расчёты параметров (синусоида)
    D, A, T, Fi = 3, 4, 24, 0
    initial_guess = [D, A, Fi]
    mu_args = minimize(obj_func, x0=initial_guess, args=(buf["mu"]))
    sigma_args = minimize(obj_func, x0=initial_guess, args=(buf["sigma"]))
    D1, A1, Fi1 = mu_args.x
    D2, A2, Fi2 = sigma_args.x
    buf["mu_appox"] = D1 + A1 * np.sin((2 * np.pi / 24) * np.arange(24) + Fi1)
    buf["sigma_appox"] = D2 + A2 * np.sin((2 * np.pi / 24) * np.arange(24) + Fi2)

    # Расчёты параметров (полином)
    # mu_p = np.poly1d(np.polyfit(buf["hour"], buf["mu"], 8))
    # buf["mu_appox"] = mu_p(buf["hour"])
    # sigma_p = np.poly1d(np.polyfit(buf["hour"], buf["sigma"], 8))
    # buf["sigma_appox"] = sigma_p(buf["hour"])

    # Генерация ряда по параметрам
    t_clean = []
    for ind in range(len(df)):
        hour = df["datetime"][ind].hour
        value = df["t_en"][ind]
        mu = D1 + A1 * np.sin((2 * np.pi / 24) * hour + Fi1)
        sigma = D2 + A2 * np.sin((2 * np.pi / 24) * hour + Fi2)
        sigma = 0
        norm_rv = sts.norm(loc=mu, scale=sigma)
        diff = norm_rv.rvs(1)[0]
        t_clean.append(value-diff)
    df.insert(3, "t_en_clean", t_clean, True)

    # График с параметрами
    # ax.plot(buf["hour"], buf["mu"], label="μ")
    # #ax.plot(buf["hour"], buf["mu_appox"], '--', label=f"аппроксимация μ, "
    # #                                            f"D={D1:.2f}, A={A1:.2f}, φ={Fi1:.2f}")
    # ax.plot(buf["hour"], buf["sigma"], label="σ")
    # #ax.plot(buf["hour"], buf["sigma_appox"], '--', label=f"аппроксимация σ, "
    # #                                               f"D={D2:.2f}, A={A2:.2f}, φ={Fi2:.2f}")
    # ax.grid()
    # ax.legend()
    # #plt.title("Изменение параметров в течении суток и наложенная аппроксимация")
    # plt.title("Изменение параметров в течении суток")
    # plt.show()

    # Коррелограмма
    # plt.scatter(df["t_en"], df["t_en_weather"])
    # plt.title("Корреллограмма между температурами по показаниям датчика и по погоде")
    # plt.xlabel("Показания датчика")
    # plt.ylabel("Погода")
    # plt.grid()
    # plt.show()

    # Основной график
    #clean_label = "Скорректированные показания датчика по вероятностной формуле"
    clean_label = "Скорректированные показания датчика по детерминистической формуле"
    plt.plot(df["datetime"], df["t_en"], label="Показания датчика")
    plt.plot(df["datetime"], df["t_en_clean"], "green", label=clean_label)
    plt.plot(df["datetime"], df["t_en_weather"], "darkorange", label="Погода")
    plt.title("Температуры по показаниям датчика и по погоде")
    plt.legend()
    plt.grid()
    plt.show()

    #df.to_excel(f"result/test.xlsx", index=False)


def permskay_reader():
    """ """

    dataPath = "data/signals/permskay_2024_10_09.csv"
    dateName = "datetime"

    data = pd.read_csv(dataPath, sep=',', decimal='.')
    buff = {}

    for guid, signal, value, datetime in data.values:
        if signal != "guard":
            continue

        dt = datetime[: datetime.rfind('.')]  # стирание микросекунд

        if signal not in buff:
            buff[signal] = {"datetime": [], "value": []}

        buff[signal]["datetime"].append(dt)
        buff[signal]["value"].append(value)

    print('Write ...')
    for signal, values in buff.items():
        df = pd.DataFrame(values)
        #df.to_excel(f"result/{signal}.xlsx", index=False)
        df.to_csv(f"result/{signal}.csv", index=False)


def create_oscillogram_1():
    """Генерация осциллограмм напряжения"""

    def create_parabola(n, turn=0):
        """Генерация параболы"""
        turn = -1 if turn else 1
        px = np.arange(-5, 5, 10 / n)
        a = -24240*turn
        c = 303000*turn
        py = 1/2 * a * pow(px, 2) + c

        return list(py)

    def create_rw(n, minVal, maxVal, step, start):
        """Генерация перенапряжения"""

        py = []
        #start = (maxVal + minVal) / 2
        for i in range(n):
            next = random.randint(-step, step)
            start += -next if (start+next) > maxVal or (start+next) < minVal else next
            py.append(start)

        return py

    def create_line(n, first, second):
        """Генерирует линию между точками"""

        step = second - first
        return list(np.arange(first, second, step/n))

    def create_interpol(dates, x, y):
        """Генерирует интерполяцию"""

        return list(np.interp(dates, x, y))

    x = []
    y = []
    x2 = []
    y2 = []

    # генерация x
    # x.extend(np.arange(0, 40, 40/5000))
    # x.extend(np.arange(40, 50, 10/1250))  # для теста
    # x2.extend(np.arange(40, 50, 10/626250))
    # x.extend(np.arange(50, 100, 50/6250))
    ###################
    x.extend(np.arange(0, 100, 100 / 12500000))

    # # генерация y
    # for i in range(3):
    #     y.extend(create_parabola(1250, i % 2))
    # y.extend(create_parabola(1250, 1)[:625])
    # y.extend(create_line(625, -303000, (428000 + 1200000) / 2))
    # #y.extend(create_rw(1250, 428000, 1200000, 100000))  # для теста
    # y2.extend(create_rw(208750, 428000, 1200000, 1000, y[-1]))
    # y2.extend(create_rw(208750, 328000, 856000, 1000, y2[-1]))
    # y2.extend(create_rw(208750, 228000, 642000, 1000, y2[-1]))
    # y.extend(create_interpol(np.arange(40, 50, 10/1250), x2, y2))  # нормализация триггера
    # y.extend(create_line(625, y[-1], -303000))
    # y.extend(create_parabola(1250, 1)[625:])
    # for i in range(4):
    #     y.extend(create_parabola(1250, i % 2))
    #####################
    for i in range(3):
        y.extend(create_parabola(1250_000, i % 2))
    y.extend(create_parabola(1250_000, 1)[:625_000])
    y.extend(create_line(625_000, -303000, (428000 + 1200000) / 2))
    y.extend(create_rw(416668, 428000, 1200000, 1000, y[-1]))
    y.extend(create_rw(416666, 328000, 856000, 1000, y[-1]))
    y.extend(create_rw(416666, 228000, 642000, 1000, y[-1]))
    y.extend(create_line(625_000, y[-1], -303000))
    y.extend(create_parabola(1250_000, 1)[625_000:])
    for i in range(4):
        y.extend(create_parabola(1250_000, i % 2))

    # График
    plt.plot(x2, y2, label="sub")
    plt.plot(x, y, label="main")
    plt.legend()
    plt.title("Осциллограмма напряжения - 3 (целевая)")
    plt.grid()
    plt.show()

    # Сохранение в файл
    savePath = "result/osc_1.txt"
    with open(savePath, "w") as f:
        # f.write("8e-6\n")
        # f.write("12500\n")
        # for item in y:
        #     f.write(f"{item}\n")
        # f.write("1.59e-8\n")
        # f.write("626250\n")
        # for item in y2:
        #     f.write(f"{item}\n")
        #####################
        f.write("8e-9\n")
        f.write("12500000\n")
        for item in y:
            f.write(f"{item}\n")


def create_oscillogram_2():
    """Генерация осциллограмм ЧР"""

    def create_noice(n, zeros, turn=0):
        """Генерация шума"""

        py = []

        for i in range(n):
            if random.randint(0, 100) < zeros:
                value = np.random.normal(1, 1)
                if turn:
                    value *= -1
                    value = value if value < 0 else 0
                else:
                    value = value if value > 0 else 0
                py.append(value)
            else:
                py.append(0)

        return py

    def create_rw(n, minVal, maxVal, step, start):
        """Генерация перенапряжения"""

        py = []
        for i in range(n):
            next = random.randint(-step, step)/10000
            if start > maxVal:
                start += -next if next > 0 else next
            elif start < minVal:
                start += next if next > 0 else -next
            else:
                start += -next if (start+next) > maxVal or (start+next) < minVal else next
            py.append(start)

        return py

    def create_interpol(dates, x, y):
        """Генерирует интерполяцию"""

        return list(np.interp(dates, x, y))

    def add_zeros(data, zeros):
        """Добавить нули"""

        py = []
        for value in data:
            if random.randint(0, 10000) < zeros:
                py.append(value)
            else:
                py.append(0)

        return py

    x = []
    y = []
    x2 = []
    y2 = []

    # генерация x
    # x.extend(np.arange(0, 40, 40/5000))
    # x.extend(np.arange(40, 50, 10/1250))  # для теста
    # x2.extend(np.arange(40, 50, 10/626250))
    # x.extend(np.arange(50, 100, 50/6250))
    ###################
    x.extend(np.arange(0, 100, 100 / 12500000))

    # генерация y
    # for i in range(4):
    #     y.extend(create_noice(1250, 1, i % 2))
    # y2.extend(create_rw(208750, 10, 20, 200, 18))
    # y2.extend(create_rw(208750, 4, 14, 200, y2[-1]))
    # y2.extend(create_rw(208750, 0, 6, 200, y2[-1]))
    # y3 = create_interpol(np.arange(40, 50, 10/1250), x2, y2)  # нормализация триггера
    # y2 = add_zeros(y2, 1)
    # y.extend(add_zeros(y3, 100))
    # for i in range(5):
    #     y.extend(create_noice(1250, 2, i % 2 == 0))
    #####################
    for i in range(4):
        y.extend(create_noice(1250_000, 1, i % 2))
    y2.extend(create_rw(416668, 10, 20, 200, 18))
    y2.extend(create_rw(416666, 4, 14, 200, y2[-1]))
    y2.extend(create_rw(416666, 0, 6, 200, y2[-1]))
    y.extend(add_zeros(y2, 200))
    for i in range(5):
        y.extend(create_noice(1250_000, 2, i % 2 == 0))

    # График
    plt.plot([], [], label="sub")
    #plt.plot(x2, y2, label="sub")
    plt.plot(x, y, label="main")
    plt.legend()
    plt.title("Осциллограмма ЧР - 3 (целевая)")
    plt.grid()
    plt.show()

    # Сохранение в файл
    savePath = "result/osc_1.txt"
    with open(savePath, "w") as f:
        # f.write("8e-6\n")
        # f.write("12500\n")
        # for item in y:
        #     f.write(f"{item}\n")
        # f.write("1.59e-8\n")
        # f.write("626250\n")
        # for item in y2:
        #     f.write(f"{item}\n")
        #####################
        f.write("8e-9\n")
        f.write("12500000\n")
        for item in y:
            f.write(f"{item}\n")


def create_oscillogram_3():
    """Генерация векторов кажущихся зарядов ЧР"""

    def create_values(n, minVal, maxVal):
        """Генерация значений"""

        py = []
        for i in range(n):
                py.append(random.randint(minVal*100, maxVal*100)/100)

        return py

    x = []
    y = []

    # генерация x
    x.extend(np.arange(0, 40, 40/10))
    x.extend(np.arange(40, 50, 10/30))
    x.extend(np.arange(50, 100, 50/10))
    ###################

    x = list(np.array(x)-40)

    # генерация y
    # y.extend(create_values(10, 1, 3))
    # y.extend(create_values(10, 15, 20))
    # y.extend(create_values(10, 10, 15))
    # y.extend(create_values(10, 8, 12))
    # y.extend(create_values(10, 1, 4))
    #####################
    y.extend(create_values(10, 1, 7))
    y.extend(create_values(10, 15, 20))
    y.extend(create_values(10, 10, 15))
    y.extend(create_values(10, 8, 12))
    y.extend(create_values(10, 1, 9))

    # График
    plt.plot(x, y, label="main")
    plt.legend()
    plt.title("Вектор кажущихся зарядов ЧР - 3 (целевой)")
    plt.grid()
    plt.show()

    # Сохранение в файл
    savePath = "result/osc_1.txt"
    with open(savePath, "w") as f:
        f.write("<Time>")
        for value in x:
            f.write(f" {np.round((value)/1000, 6)}")
        f.write("</Time>\n")
        f.write("<AC>")
        for value in y:
            f.write(f" {np.round(value, 6)}")
        f.write("</AC>")


def show_data():
    """ """

    path = "data/24-07-19/TrendControl АТ2.csv"
    dt = pd.read_csv(path, sep=';', decimal=',')

    columns = dt.columns
    dt[columns[0]] = pd.to_datetime(dt[columns[0]])

    plt.plot(dt[columns[0]], dt["c_ch4"], label="c_ch4")
    plt.plot(dt[columns[0]], dt["c_co2"], label="c_co2")

    #for col in columns:
    #    if col == columns[0]:
    #        continue
    #    plt.plot(dt[columns[0]], dt[col], label=col)

    plt.legend()
    plt.grid()
    plt.title("AT-2")
    plt.show()


def correct_excel():
    """Переименование и перетаскивание заголовков для больших файлов"""

    root = "data/exel"
    name = "083.xlsx"

    path = os.path.join(root, name)
    print(f"Read - {path}")
    df = pd.read_excel(path)

    correct = [
        "datetime",
        "c_h2",
        "c_o2",
        "c_n2",
        "c_co",
        "c_co2",
        "c_ch4",
        "c_c2h2",
        "c_c2h4",
        "c_c2h6",
        "rs",
        "wcl",
        "t_bt",
        "t_tp",
        "t_lt",
    ]

    df_new = pd.DataFrame()

    for col in correct:
        print(f"Correct - {col}")
        df_new[col] = df[col]

    print("Write")
    df_new.to_excel(f"result/correct.xlsx", index=False)
    print("Done")


def combinator():
    """Комбинатор параметров"""

    # np.linspace()

    # Параметры для комбинаций
    params = {
        # "t_en": list(range(-30, 50, 5)),
        # "i_hv_pa": list(np.arange(0.79*100, 2.1655*100, 0.0655*100)),
        # "hi_insulation": [40, 60, 100],
        # "pdata_yr": [2020, 1980],
        # "f_overload_permitted": [1, 0],
        # "pdata_s": [16000, 40000],
        # "pdata_cooling_type": ['М', 'Д', 'ДЦ'],
        # "pdata_i_hv": [100],

        # "albatros_koh_offline": [0.008, 0.016],
        # "wcp": [0.5, 1],
        # "t_hst": range(0, 220, 20),
        # "f_outage": [1, 0],
        # "f_paper_thermally_upgraded": [1, 0],
        #
        # "wcp_rated": [0.5],
        # "k_power_ageing_wcp": [1.493],
        # "k_power_ageing_koh": [1.05],
        # "koh_rated": [1.008],
    }
    # Параметры для клонирования
    clones = {
        # "i_hv_pa": ["i_hv_pb", "i_hv_pc"],
        # "hi_insulation": ["hi_magcore", "hi_winding"],
    }

    # Генерация меток времени
    startTime = datetime.strptime("01.01.2022", "%d.%m.%Y")
    stepTime = timedelta(hours=1)  # seconds, minutes, hours
    timelen = 4344  # np.prod([len(p) for p in params.values()])
    dates = [startTime + stepTime * i for i in range(timelen)]

    data = {key: [] for key in params}
    keys = list(params.keys())

    # Перебор параметров
    for values in product(*params.values()):
        for ind in range(len(keys)):
            data[keys[ind]].append(values[ind])

    # Клонирование параметров
    for key, columns in clones.items():
        for col in columns:
            data[col] = copy(data[key])

    count = 4344
    data = {
        "с_co": np.linspace(0, 1600, count),
        "с_co2": np.linspace(14000, 0, count),
        "с_h2": np.linspace(0, 340, count),
        "с_ch4": np.linspace(0, 520, count),
        "с_c2h4": np.linspace(0, 300, count),
        "с_c2h6": np.linspace(0, 360, count),
        "с_c2h2": np.linspace(0, 120, count),

        "bush_c1_20_pa": np.linspace(21000, 25200, count),
        "bush_c1_20_pb": np.linspace(21000, 25200, count),
        "bush_c1_20_pc": np.linspace(21000, 25200, count),
        "bush_tgd_20_pa": np.linspace(21000, 25200, count),
        "bush_tgd_20_pb": np.linspace(21000, 25200, count),
        "bush_tgd_20_pc": np.linspace(21000, 25200, count),
    }

    # Сохранение
    df = pd.DataFrame(data)
    df.insert(0, "datetime", dates)
    df.to_excel(f"result/test/test.xlsx", index=False)


def combinator_v2():
    """Комбинатор параметров"""

    # Параметры для генерации
    genParams = {
        "t_tp": np.linspace(-20, 80, 6),
        "t_bt": np.linspace(-20, 80, 6),
        "с_co": np.linspace(0, 1600, 6),
        "с_co2": np.linspace(14000, 0, 6),
        "с_h2": np.linspace(0, 340, 6),
        "с_ch4": np.linspace(0, 520, 6),
        "с_c2h4": np.linspace(0, 300, 6),
        "с_c2h6": np.linspace(0, 360, 6),
        "с_c2h2": np.linspace(0, 120, 6),
        "rs": np.linspace(0.1, 4, 6),
        "bush_tgd_pa": np.linspace(0.1, 4, 6),
        "bush_tgd_pb": np.linspace(0.1, 4, 6),
        "bush_tgd_pc": np.linspace(0.1, 4, 6),
        "bush_c1_pa": np.linspace(21000, 25200, 6),
        "bush_c1_pb": np.linspace(21000, 25200, 6),
        "bush_c1_pc": np.linspace(21000, 25200, 6)
    }

    # Параметры для комбинаций
    combParams = {
        "pdata_oil_protection": ["Свободное дыхание", "Плёночная, Азотная"],
        "pdata_oil_type": ["ГК", "Nytro", "Смесь"],
        "life": [1, 50],
        "pdata_u_hv": [35, 110, 220, 500],
        "pdata_ltc_type": ["RS - 3", "Другие"],
        "pdata_s": [16, 40],
        "pdata_bush": ["Бумажно - масляная", "Твёрдая с масляным заполнением",
                       "Бумажно - бакелитовая с мастичным заполнением", "RIP"],

        "albatros_its_fuz2": [50],
        "albatros_its_fuz3": [50],
        "albatros_its_fuz4": [50],
        "t_en": [30],
        "bush_c1_lim1": [22050],
        "add_h20": [1],
        "k_fu_1085": [0.18],
        "k_fu_1044": [0.32],
        "k_fu_995": [0.25],
        "k_fu_1081": [0.18],
        "k_gpfu_1091": [0.29],
        "k_gpfu_1044": [0.5],
        "k_gpfu_1058": [0.5],
        "k_gpfu_1015": [0.5],
        "k_arr_a": [7.11],
        "k_arr_b": [1820],
        "wcl_rell_rec_lim0": [1],
        "wcl_rell_rec_lim1": [5],
        "c_roc_h2_rel_lim0": [5],
        "c_roc_co_rel_lim0": [5],
        "c_roc_co2_rel_lim0": [5],
        "c_roc_ch4_rel_lim0": [5],
        "c_roc_c2h4_rel_lim0": [5],
        "c_roc_c2h6_rel_lim0": [5],
        "c_roc_c2h2_rel_lim0": [5],
        "c_roc_h2_rel_lim1": [10],
        "c_roc_co_rel_lim1": [10],
        "c_roc_co2_rel_lim1": [10],
        "c_roc_ch4_rel_lim1": [10],
        "c_roc_c2h4_rel_lim1": [10],
        "c_roc_c2h6_rel_lim1": [10],
        "c_roc_c2h2_rel_lim1": [10],
        "replace": range(6),
    }

    # Генерация меток времени
    startTime = datetime.strptime("01.01.2022", "%d.%m.%Y")
    stepTime = timedelta(hours=4)  # seconds, minutes, hours
    timelen = np.prod([len(p) for p in combParams.values()])
    dates = [startTime + stepTime * i for i in range(timelen)]

    # Перебор параметров
    keys = list(combParams.keys())
    buff = {key: [] for key in keys}
    for values in product(*combParams.values()):
        for ind in range(len(keys)):
            buff[keys[ind]].append(values[ind])

    # Объединение параметров
    data = {key: [] for key in list(genParams.keys()) + list(buff.keys())[:-1]}
    for ind in range(timelen):
        rep = buff["replace"][ind]
        # Заполнение генерируемых параметров
        for key in genParams:
            data[key].append(genParams[key][rep])
        # Заполнение перебираемых параметров
        for key in list(buff.keys())[:-1]:
            data[key].append(buff[key][ind])

    # Сохранение
    df = pd.DataFrame(data)
    df.insert(0, "datetime", dates)
    df.to_excel(f"result/test/test.xlsx", index=False)


def test2():
    """Тест чтения бекапов"""

    from subprocess import PIPE, Popen, run

    ls_output = Popen(["src/simple.py"])
    ls_output.communicate()


def analiz():
    """ """

    # Заголовки и данные детальной аналитики
    passed = {
        "substation": [],
        "asset": [],
        #"code": [],
        "code": [],
        "name": [],
        "source": [],
        "status": [],
        "values_count": [],
        "values_unique": [],
        "value_first": [],
        "datetime_first": [],
        "value_last": [],
        "datetime_last": [],
    }
    current_dt = datetime(2025, 1, 20)

    # Статусы
    correct = "Корректные"
    incorrect = "Ошибочные"
    old = "Старые"
    absent = "Не передаются"

    # Пути к файлам с данными
    root = "data\\exel"
    files = [
        #["ПС Белый Раст", "ПС Белый Раст.xlsx"],
        #["ПС Бескудниково", "ПС Бескудниково.xlsx"],
        #["ПС Звёздная", "ПС Звёздная.xlsx"],
        #["ПС Ленинградская", "ПС Ленинградская.xlsx"],
        ["ПС Очаково", "ПС Очаково.xlsx"],
        #["ПС Пахра", "ПС Пахра.xlsx"],
    ]

    # Обход подстанций
    for pc, file in files:
        print(f"\n=======")
        print(f"{pc}:")
        dataPath = os.path.join(root, file)
        name = "Сигналы подстанций.xlsx"
        signalsPath = os.path.join(root, name)
        assets = names.all_assets[pc]

        # чтение данных
        print(f"Read datas - {dataPath}")
        df = pd.read_excel(dataPath)
        df.sort_values("date_time", inplace=True)
        print(f"Read signals - {signalsPath}")
        df_signals = pd.read_excel(signalsPath, sheet_name=pc)

        # сигналы объектов в таблице сигналов
        valid_signals = {}
        for asset in assets:
            signals = df_signals[df_signals["asset"] == asset]
            signals = signals[signals["source"] != "Расчётный"]
            #signals = signals[signals["source"] == "КИВ-500"]
            #valid_signals[asset] = list(signals["code"])
            valid_signals[asset] = list(signals.values)

        # обход
        for asset in assets:
            print(f"Обработка - {asset}")
            for _, code, signal_name, source in valid_signals[asset]:
                # игнорировать?
                if "lim1" in code or "lim0" in code:
                    continue

                data = df[df["asset"] == asset]
                data = data[data["signal_code"] == code]

                passed["substation"].append(pc)
                passed["asset"].append(asset)
                passed["code"].append(code)
                passed["name"].append(signal_name)
                passed["source"].append(source)

                # данные есть?
                if len(data):
                    values = list(data["value"])
                    dates = list(data["date_time"])
                    unicvalues = set(data["value"])
                    passed["values_count"].append(len(values))
                    passed["values_unique"].append(len(unicvalues))
                    passed["value_first"].append(values[0])
                    passed["datetime_first"].append(dates[0])
                    passed["value_last"].append(values[-1])
                    passed["datetime_last"].append(dates[-1])
                    # старые данные
                    if dates[-1] < current_dt:
                        passed["status"].append(old)
                    # данные меняются
                    elif len(unicvalues) > 2 \
                            or code.startswith("cooling") or code.startswith("counter"):
                        passed["status"].append(correct)
                    # данные не меняются
                    else:
                        passed["status"].append(incorrect)
                # данных нет
                else:
                    passed["values_count"].append(None)
                    passed["values_unique"].append(None)
                    passed["value_first"].append(None)
                    passed["datetime_first"].append(None)
                    passed["value_last"].append(None)
                    passed["datetime_last"].append(None)
                    passed["status"].append(absent)

    # вывод результатов в эксель
    name = f"аналитика"
    print(f'Write to {root}/{name}.xlsx ...')
    df = pd.DataFrame(passed)
    df.to_excel(f"{root}/{name}.xlsx", index=False)
    print('Done')


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


def exp_trend_log(x, y):
    """Вычисление параметров экспоненциального тренда"""
    # чистим
    x = pd.to_numeric(x, errors="coerce").to_numpy(float)
    y = pd.to_numeric(y, errors="coerce").to_numpy(float)

    m = np.isfinite(x) & np.isfinite(y) & (y > 0)
    x = np.asarray(x)[m]
    y = np.asarray(y)[m]

    # ln(y) = ln(a) + b*x
    b, ln_a = np.polyfit(x, np.log(y), 1)
    a = np.exp(ln_a)

    # качество
    y_hat = a * np.exp(b * x)
    ss_res = np.sum((y - y_hat) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return a, b, r2


def calc_wcl_test():
    """Расчёт кривых Ройзмана"""

    A = [5.55201183628544, 3.550143363628681, 2.6124613519000515]
    D = [-9.241908539822525, -5.250873492708096, -1.1645318138407346]
    F = [118.01981471458994, 106.5273381544408, 149.3079002660737]
    T = [283.610016850824, 270.41137812081746, 351.759407577563]

    t = np.arange(0.0, 110.1, 0.1)
    wcp = np.arange(0.1, 5.1, 0.1)  # [1, 2, 4]
    result = {"t": np.arange(0.0, 110.1, 0.1)}

    for i in wcp:
        i = np.round(i, 1)
        print(f"wcp = {i}")
        result[f"wcl_{i}"] = []
        end = False
        for j in t:
            a = np.exp(D[0] + A[0]*np.sin(2*np.pi*j/T[0] + 2*np.pi/T[0]*F[0]))
            b = np.exp(D[1] + A[1]*np.sin(2*np.pi*j/T[1] + 2*np.pi/T[1]*F[1]))
            c = np.exp(D[2] + A[2]*np.sin(2*np.pi*j/T[2] + 2*np.pi/T[2]*F[2]))
            roots = np.roots([a, -b, c, -i])
            root = roots[2]
            if not np.isclose(root.imag, 0):
                end = True
            if not end:
                result[f"wcl_{i}"].append(root.real)
            else:
                result[f"wcl_{i}"].append(None)
            #if root
            #    result[f"wcl_{i}"].append(roots[2].real)

            #result[f"wcl_{i}"].append(None)
            #for idx, root in enumerate(roots):
            #    if np.isclose(root.imag, 0) and root.real > 0 and root.real < 200:
            #        result[f"wcl_{i}"][-1] = root.real

    # rs 100%
    # for j in t:
    #     wcl_100 = np.power(10, 7.23 - 1640 / (j + 273.15))
    #     result[f"wcl_1"].append(None)
    #     result[f"wcl_2"].append(None)
    #     result[f"wcl_3"].append(wcl_100)
    #     result["wcp"].append(100)
    #     result["t"].append(j)

    # подсчёт параметров экспонент

    df = pd.DataFrame(result)
    exp_result = {"wcp": [], "A": [], "B": [], "r2": []}

    for i in wcp:

        i = np.round(i, 1)
        x = df["t"]
        y = df[f"wcl_{i}"]
        a, b, r2 = exp_trend_log(x, y)
        exp_result["wcp"].append(i)
        exp_result["A"].append(a)
        exp_result["B"].append(b)
        exp_result["r2"].append(r2)

    print(f'Write to result/wcl_test.xlsx ...')
    df = pd.DataFrame(exp_result)
    df.to_excel(f"result/wcl_test.xlsx", index=False)
    print('Done')


def calc_wcl(t, wcp):
    """Расчёт кривых Ройзмана"""

    a = 1.21801 * wcp - 0.12651
    b = -0.00055 * wcp ** 2 + 0.00592 * wcp + 0.03562
    wcl = a * np.exp(b * t)

    return wcl


def find_exponential_tangent(t, wcl, wcp_lo=0.1, wcp_hi=10.0, iters=80):
    """
    Находит экспоненциальную касательную к облаку точек (x, y > 0)
    Касательная проходит через ровно одну точку и лежит снаружи остальных

    upper: минимальный wcp, при котором f_curve(t, wcp) >= y для всех точек (кривая выше облака)
    lower: максимальный wcp, при котором f_curve(t, wcp) <= y для всех точек (кривая ниже облака)

    Возвращает: (wcp_lower, wcp_upper)
    """

    # фильтр точек
    t = np.asarray(t, dtype=float)
    y = np.asarray(wcl, dtype=float)
    m = np.isfinite(t) & np.isfinite(y)
    t, y = t[m], y[m]
    if t.size == 0:
        raise ValueError("Нет валидных точек после фильтрации NaN/inf.")

    # функции нарушений: <= 0 значит условие выполнено
    def viol_upper(w):  # хотим f >= y
        return np.max(y - calc_wcl(t, w))

    def viol_lower(w):  # хотим f <= y
        return np.max(calc_wcl(t, w) - y)

    # --- upper: минимальный w, где viol_upper(w) <= 0
    v_lo = viol_upper(wcp_lo)
    v_hi = viol_upper(wcp_hi)
    if v_hi > 0:
        raise ValueError("Upper не найден: даже при wcp_hi кривая ниже некоторых точек. Увеличь wcp_hi.")
    if v_lo <= 0:
        wcp_upper = wcp_lo
    else:
        lo, hi = wcp_lo, wcp_hi
        for _ in range(iters):
            mid = (lo + hi) / 2
            if viol_upper(mid) <= 0:
                hi = mid
            else:
                lo = mid
        wcp_upper = hi

    # --- lower: максимальный w, где viol_lower(w) <= 0
    v_lo = viol_lower(wcp_lo)
    v_hi = viol_lower(wcp_hi)
    if v_lo > 0:
        raise ValueError("Lower не найден: уже при wcp_lo кривая выше некоторых точек. Уменьши wcp_lo.")
    if v_hi <= 0:
        wcp_lower = wcp_hi
    else:
        lo, hi = wcp_lo, wcp_hi
        for _ in range(iters):
            mid = (lo + hi) / 2
            if viol_lower(mid) <= 0:
                lo = mid  # условие ещё держится, можно выше
            else:
                hi = mid
        wcp_lower = lo

    return wcp_lower, wcp_upper


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


if __name__ == '__main__':
    #dataSelector()

    # files = [
    #     #[r'data/Парковая аналитика/Западная/Т-1', 'Западная-Т-1'],
    # ]
    #
    # for item in files:
    #     combineData(item[0], item[1])

    #parse_obscure()
    #upsamplingData()
    #correlations()
    #absoluteGrowthRate()
    #test_3D()
    #add_anomaly()
    #mapping()
    #permskay_reader()
    #create_signals()
    #create_oscillogram_1()
    #create_oscillogram_2()
    #create_oscillogram_3()
    #analiz()

    #show_data()
    #correct_excel()

    #combinator()
    #combinator_v2()
    test2()
