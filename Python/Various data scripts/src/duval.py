# -*- coding: utf-8 -*-
"""

(С) 2025 БО-Энерго,
"""
# ---- BUILT ----
import random

# ---- OUTER ----
import pandas as pd
import numpy as np

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def duval_4(c_h2, c_ch4, c_c2h6):
    """Расчёт зон для треугольника Дюваля 4"""

    r_h2: float = 100 * c_h2 / (c_h2 + c_ch4 + c_c2h6)
    r_ch4: float = 100 * c_ch4 / (c_h2 + c_ch4 + c_c2h6)
    r_c2h6: float = 100 - r_ch4 - r_h2

    if 2 <= r_ch4 <= 15 and r_c2h6 <= 1:
        return "PD"
    elif (r_h2 >= 41 and r_ch4 <= 36 and r_c2h6 <= 25) or \
         (15 <= r_h2 <= 75 and r_ch4 <= 60 and 24 <= r_c2h6 <= 30) or \
         (9 <= r_h2 <= 70 and r_ch4 <= 61 and 30 <= r_c2h6 <= 46):
        return "S"
    elif r_c2h6 <= 30:
        return "C"
    elif r_h2 <= 9 and r_ch4 <= 70 and r_c2h6 >= 30:
        return "O"
    else:
        return "ND"


def duval_5(c_ch4, c_c2h4, c_c2h6):
    """Расчёт зон для треугольника Дюваля 5"""

    r_ch4: float = 100 * c_ch4 / (c_ch4 + c_c2h4 + c_c2h6)
    r_c2h4: float = 100 * c_c2h4 / (c_ch4 + c_c2h4 + c_c2h6)
    r_c2h6: float = 100 - r_c2h4 - r_ch4

    if r_c2h4 <= 1 and 2 <= r_c2h6 <= 15:
        return "PD"
    elif 53 <= r_ch4 <= 90 and 10 <= r_c2h4 <= 35 and r_c2h6 <= 12:
        return "T2"
    elif (20 <= r_ch4 <= 78 and 10 <= r_c2h4 <= 50 and 12 <= r_c2h6 <= 30) or \
         (r_ch4 <= 37 and 50 <= r_c2h4 <= 70 and 13 <= r_c2h6 <= 30):
        return "C"
    elif (r_ch4 >= 75 and r_c2h4 <= 10 and r_c2h6 <= 15) or \
         (r_ch4 <= 46 and r_c2h4 <= 10 and r_c2h6 >= 54):
        return "O"
    elif 36 <= r_ch4 <= 85 and r_c2h4 <= 10 and 15 <= r_c2h6 <= 54:
        return "S"
    elif r_ch4 <= 65 and r_c2h4 >= 35 and r_c2h6 <= 60:
        return "T3"
    else:
        return "ND"


def pentagon_2(c_h2, c_ch4, c_c2h2, c_c2h4, c_c2h6):
    """ """

    import math

    gas_sum = c_h2 + c_ch4 + c_c2h2 + c_c2h4 + c_c2h6

    r_h2: float = 100 * c_h2 / gas_sum
    r_ch4: float = 100 * c_ch4 / gas_sum
    r_c2h2: float = 100 * c_c2h2 / gas_sum
    r_c2h4: float = 100 * c_c2h4 / gas_sum
    r_c2h6: float = 100 * c_c2h6 / gas_sum

    r_h2_x = 0
    r_h2_y = r_h2

    r_ch4_x = r_ch4 * math.cos((234 / 180) * math.pi)
    r_ch4_y = r_ch4 * math.sin((234 / 180) * math.pi)

    r_c2h4_x = r_c2h4 * math.cos((306 / 180) * math.pi)
    r_c2h4_y = r_c2h4 * math.sin((306 / 180) * math.pi)

    r_c2h6_x = r_c2h6 * math.cos((162 / 180) * math.pi)
    r_c2h6_y = r_c2h6 * math.sin((162 / 180) * math.pi)

    r_c2h2_x = r_c2h2 * math.cos((18 / 180) * math.pi)
    r_c2h2_y = r_c2h2 * math.sin((18 / 180) * math.pi)

    A: float = (
                       (r_h2_x * r_c2h6_y - r_c2h6_x * r_h2_y) +
                       (r_c2h6_x * r_ch4_y - r_ch4_x * r_c2h6_y) +
                       (r_ch4_x * r_c2h4_y - r_c2h4_x * r_ch4_y) +
                       (r_c2h4_x * r_c2h2_y - r_c2h2_x * r_c2h4_y) +
                       (r_c2h2_x * r_h2_y - r_h2_x * r_c2h2_y)
               ) / 2

    c_x: float = (
                         (r_h2_x + r_c2h6_x) * (r_h2_x * r_c2h6_y - r_c2h6_x * r_h2_y) +
                         (r_c2h6_x + r_ch4_x) * (r_c2h6_x * r_ch4_y - r_ch4_x * r_c2h6_y) +
                         (r_ch4_x + r_c2h4_x) * (r_ch4_x * r_c2h4_y - r_c2h4_x * r_ch4_y) +
                         (r_c2h4_x + r_c2h2_x) * (r_c2h4_x * r_c2h2_y - r_c2h2_x * r_c2h4_y) +
                         (r_c2h2_x + r_h2_x) * (r_c2h2_x * r_h2_y - r_h2_x * r_c2h2_y)
                 ) / (6 * A)

    c_y: float = (
                         (r_h2_y + r_c2h6_y) * (r_h2_x * r_c2h6_y - r_c2h6_x * r_h2_y) +
                         (r_c2h6_y + r_ch4_y) * (r_c2h6_x * r_ch4_y - r_ch4_x * r_c2h6_y) +
                         (r_ch4_y + r_c2h4_y) * (r_ch4_x * r_c2h4_y - r_c2h4_x * r_ch4_y) +
                         (r_c2h4_y + r_c2h2_y) * (r_c2h4_x * r_c2h2_y - r_c2h2_x * r_c2h4_y) +
                         (r_c2h2_y + r_h2_y) * (r_c2h2_x * r_h2_y - r_h2_x * r_c2h2_y)
                 ) / (6 * A)

    d295_1: int = d295(
        a_x=c_x,
        a_y=c_y,
        poly_1_x=[-21.5, -11, -3.5, -1, 0,  -35],   # T1 -> O
        poly_1_y=[-32,   -8,  -3,   -2, 1.5, 3],
        poly_2_x=[0, 38, 32, 4, 0],                 # D1
        poly_2_y=[40, 12, -6, 16, 1.5],
        poly_3_x=None,  #
        poly_3_y=None,
        poly_4_x=[0, 0, -1, -1],                    # PD
        poly_4_y=[24.5, 33, 33, 24.5],
        poly_5_x=None,  #
        poly_5_y=None,
        poly_6_x=None,  #
        poly_6_y=None,
        poly_7_x=[2.5, -3.5, -11, -21.5],           # T2 -> C
        poly_7_y=[-32, -3,   -8,  -32],
        poly_8_x=[24,  -3.5, 2.5],                  # T3 -> T3-H
        poly_8_y=[-30, -3,  -32],
        poly_9_x=[4, 32, 24, -1],                   # D2
        poly_9_y=[16, -6, -30, -2],
    )
    level = d295_1

    return level

    #if (68 <= r_h2 <= 98 and r_c2h2 <= 15 and 2 <= r_c2h6 <= 17):
    #    return "PD"


def d295(
    a_x: float,
    a_y: float,
    poly_1_x: list[float] | None,
    poly_1_y: list[float] | None,
    poly_2_x: list[float] | None,
    poly_2_y: list[float] | None,
    poly_3_x: list[float] | None,
    poly_3_y: list[float] | None,
    poly_4_x: list[float] | None,
    poly_4_y: list[float] | None,
    poly_5_x: list[float] | None,
    poly_5_y: list[float] | None,
    poly_6_x: list[float] | None,
    poly_6_y: list[float] | None,
    poly_7_x: list[float] | None,
    poly_7_y: list[float] | None,
    poly_8_x: list[float] | None,
    poly_8_y: list[float] | None,
    poly_9_x: list[float] | None,
    poly_9_y: list[float] | None,
) -> int | None:
    """Д295. Защита 9 ст. Полигональный компаратор

    Args:
        a_x (float): Координаты в пространстве состояний
        a_y (float): Координаты в пространстве состояний

        poly_{n}_x (list(float) | None): Координаты вершин полигона n
        poly_{n}_y (list(float) | None): Координаты вершин полигона n

    Returns:
        level (int): Максимальный номер сработавшей ступени
    """

    if a_x is None or a_y is None:
        return None

    d101_1: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_1_x, poly_y=poly_1_y)
    d101_2: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_2_x, poly_y=poly_2_y)
    d101_3: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_3_x, poly_y=poly_3_y)
    d101_4: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_4_x, poly_y=poly_4_y)
    d101_5: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_5_x, poly_y=poly_5_y)
    d101_6: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_6_x, poly_y=poly_6_y)
    d101_7: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_7_x, poly_y=poly_7_y)
    d101_8: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_8_x, poly_y=poly_8_y)
    d101_9: int = d101(point_x=a_x, point_y=a_y, poly_x=poly_9_x, poly_y=poly_9_y)

    if d101_9 == 1:
        level = "D2"
    elif d101_8 == 1:
        level = "T3-H"
    elif d101_7 == 1:
        level = "C"
    elif d101_6 == 1:
        level = 6
    elif d101_5 == 1:
        level = 5
    elif d101_4 == 1:
        level = "PD"
    elif d101_3 == 1:
        level = 3
    elif d101_2 == 1:
        level = "D1"
    elif d101_1 == 1:
        level = "O"
    else:
        level = 0

    return level


def d101(
        poly_x: list[float] | None,
        poly_y: list[float] | None,
        point_x: float,
        point_y: float,
) -> int:
    """Д101. Проверка принадлежности точки многоугольнику.

    Args:
        poly_x (list[float] | None): Массив координат вершин многоугольника
        poly_y (list[float] | None): Массив координат вершин многоугольника
        point_x (float): Координаты точки
        point_y (float): Координаты точки

    Returns:
        level (int): Сигнал принадлежности точки области, описанной многоугольником
        ("1" - принадлежит; "0" - не принадлежит)
    """

    from shapely.geometry import Point, Polygon

    if poly_x is None or poly_y is None or len(poly_x) == 0:
        return 0

    # Проверяем, что массивы с координатами вершин заданы корректно
    if len(poly_x) != len(poly_y):
        raise ValueError("Lengths of poly_x and poly_y are not equal!")

    # Create Point objects
    point = Point(point_x, point_y)

    coords = [(poly_x[i], poly_y[i]) for i in range(len(poly_x))]
    poly = Polygon(coords)

    # PIP test with 'contains'
    return int(poly.buffer(0.000000001).contains(point))


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def gen_defects_gas_1():
    """ """

    #dt = np.round(np.arange(1440, 10080+1, 8640 / 7))
    dt = np.round(np.arange(0, 1440+1, 1440 / 3))
    dates_short = np.round(np.arange(dt[0], dt[-1]+1, 1440 / 10))
    dates = np.arange(dt[0], dt[-1]+1, 1)
    edges = {
        # S -> PD -> D1 -> D2 -> T3-H -> C -> O -> S
        "h2": [45, 40, 48, 45],
        "ch4": [10, 3, 7, 10],
        "c2h2": [0, 8, 5, 0],
        "c2h4": [0, 6, 2, 0],
        "c2h6": [45, 30, 37, 45],
    }
    result = {"dt": dates}
    #ref_points = {"dt": dates_short}

    # Первичное заполнение между вершинами
    for gas, vals in edges.items():
        result[gas] = np.interp(dates_short, dt, vals)
        #ref_points[gas] = np.interp(dates_short, dt, vals)

    # Добавляем шум
    for gas, vals in result.items():
        if gas == "dt":
            continue
        for i in range(len(vals)):
            if dates_short[i] not in dt:
                val = result[gas][i]
                new_val = max(np.round(val + (np.random.normal(0, 4)), 2), 0)
                result[gas][i] = new_val
                #ref_points[gas][i] = new_val

    # вторичное заполнение между вершинами
    for gas, vals in result.items():
        if gas == "dt":
            continue
        result[gas] = np.interp(dates, dates_short, vals)

    df = pd.DataFrame(result)
    df.to_excel(f"result/duval_2.xlsx", index=False)
    print('Done')

    #df = pd.DataFrame(ref_points)
    #for vals in df.values:
    #    print(f"2000/01/01,{vals[1]},{vals[2]},{vals[3]},{vals[4]},{vals[5]}")


def gen_defects_gas_2():
    """ """

    dt = np.round(np.arange(1440, 10080+1, 8640 / 7))
    #dt = np.round(np.arange(0, 70+1, 10))
    dates_short = np.round(np.arange(dt[0], dt[-1]+1, 8640 / 100))
    dates = np.arange(dt[0], dt[-1]+1, 1)
    edges = {
        # S -> PD -> D1 -> D2 -> T3-H -> C -> O -> S
        #"h2": [45, 82, 45, 20, 0, 0, 0, 45],
        #"ch4": [10, 0, 0, 0, 10, 50, 40, 10],
        #"c2h2": [0, 8, 45, 35, 0, 0, 20, 0],
        #"c2h4": [0, 0, 10, 35, 60, 30, 0, 0],
        #"c2h6": [45, 10, 0, 10, 30, 20, 40, 45],
        "co2": [1853.639, 2760.633, 2660.314, 2360.61, 2860.687, 2560.314, 2460.76, 1853.639],
    }
    result = {"dt": dates}
    ref_points = {"dt": dates_short}

    # Первичное заполнение между вершинами
    for gas, vals in edges.items():
        result[gas] = np.interp(dates_short, dt, vals)
        ref_points[gas] = np.interp(dates_short, dt, vals)

    # Добавляем шум
    noice = 40  # 4
    for gas, vals in result.items():
        if gas == "dt":
            continue
        for i in range(len(vals)):
            if dates_short[i] not in dt:
                val = result[gas][i]
                new_val = max(np.round(val + (np.random.normal(0, noice)), 2), 0)
                result[gas][i] = new_val
                ref_points[gas][i] = new_val

    # вторичное заполнение между вершинами
    for gas, vals in result.items():
        if gas == "dt":
            continue
        result[gas] = np.interp(dates, dates_short, vals)

    df = pd.DataFrame(result)
    df.to_excel(f"result/duval_2.xlsx", index=False)
    print('Done')

    #df = pd.DataFrame(ref_points)
    #for vals in df.values:
    #    print(f"2000/01/01,{vals[1]},{vals[2]},{vals[5]},{vals[4]},{vals[3]}")


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def main():
    """ """

    # while True:
    #     h2 = random.randint(0, 100)
    #     ch4 = random.randint(0, 100-h2)
    #     c2h6 = 100-(h2+ch4)
    #     print(f"[{h2}, {ch4}, {c2h6}] ({sum([h2, ch4, c2h6])}) -> {duval_4(h2, ch4, c2h6)}")
    #     input("")

    # while True:
    #     ch4 = random.randint(0, 100)
    #     c2h4 = random.randint(0, 100-ch4)
    #     c2h6 = 100-(ch4+c2h4)
    #     print(f"[{ch4}, {c2h4}, {c2h6}] ({sum([ch4, c2h4, c2h6])}) -> {duval_5(ch4, c2h4, c2h6)}")
    #     input("")

    i = 0
    while i <= 100:
        h2 = random.randint(0, 1000)
        ch4 = random.randint(0, 1000-h2)
        c2h2 = random.randint(0, 1000-h2-ch4)
        c2h4 = random.randint(0, 1000-h2-ch4-c2h2)
        c2h6 = 1000-(h2+ch4+c2h2+c2h4)
        h2 = max(h2/10, 0.1)
        ch4 = max(ch4/10, 0.1)
        c2h2 = max(c2h2/10, 0.1)
        c2h4 = max(c2h4/10, 0.1)
        c2h6 = max(c2h6/10, 0.1)
        zone = pentagon_2(h2, ch4, c2h2, c2h4, c2h6)
        #if zone in ["C", "O", "T3-H"]:
        if zone in ["C"]:
            i += 1
            print(f"2000/01/1,{h2},{ch4},{c2h6},{c2h4},{c2h2}")
            #print(f"[{h2}, {ch4}, {c2h6}, {c2h4}, {c2h2}] ({sum([h2, ch4, c2h6, c2h4, c2h2])}) -> "
            #      f"{zone}")
            #input("")


if __name__ == '__main__':
    #main()
    #gen_defects_gas_1()
    gen_defects_gas_2()


# 1 - T1
# 2 - D1
# 3 -
# 4 - PD
# 5 -
# 6 -
# 7 - T2
# 8 - T3
# 9 - D2
#
