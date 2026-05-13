# -*- coding: utf-8 -*-
"""
interpol.py — модуль интерполяции и обработки временных рядов

Описание:
    Модуль предоставляет инструменты для:
    - чтения и подготовки данных из CSV/XLSX
    - преобразования дат в excel-числа и обратно
    - интерполяции временных рядов
    - генерации синхронизированных временных сеток

Примечания:
    Формат дат на входе предполагается строковым, преобразуется в excel-style float.
    Выходные файлы можно сохранять в .csv или .xlsx.
    Работает с pandas, numpy, datetime.
    Поддерживает обработку отсутствующих данных и агрегацию по временным меткам.
    Пользуйтесь на свой страх и риск.

(С) 2025 БО-Энерго, Альфред Дж. Киттелл
"""

# ---- BUILT ----
import os
from copy import deepcopy
from datetime import datetime, timedelta

# ---- OUTER ----
import pandas as pd
import numpy as np

###########################################################


def frames_interpolation(frames, dates, dateName) -> dict:
    """
    Объединение фреймов с помощью интерполяции

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dates : list, ndarray
        Список дат
    dateName : str
        Какой заголовок считать датой
    """

    for frame in frames:
        try:
            if len(frames[frame]):
                frames[frame] = np.interp(dates, frames[frame][dateName], frames[frame][frame])
                frames[frame] = frames[frame].round(3)
            else:
                frames[frame] = [None for _ in range(len(dates))]
        except:
            print(f"{frame} - сломался")

    return frames


def frames_combine(frames, dates) -> dict:
    """
    Объединение фреймов с сохранением исходных значений

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dates : list, ndarray
        Список дат
    """

    # Подготовка
    data = {dt: None for dt in dates}

    # Заполнение
    for frame in frames:
        _data = deepcopy(data)
        for dt, value in frames[frame].values:
            _data[dt] = value
        frames[frame] = _data.values()

    return frames


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def dates_generation(frames, dateName, step, dateStart=None, dateEnd=None):
    """
    Генерация списка дат с шагом

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dateName : str
        Какой заголовок считать датой
    step : float
        Шаг данных - 1 - 1 день, 1/24 - 1 час, 1/48 - 30 минут, 1/17280 - 5 сек
    dateStart : float, datetime, optional
        Начальная дата генерации, если нужно задать вручную
    dateEnd : float, datetime, optional
        Конечная дата генерации, если нужно задать вручную
    """

    # Определяем начало в датах
    if dateStart is not None:
        if isinstance(dateStart, float):
            start = dateStart
        elif isinstance(dateStart, datetime):
            delta = dateStart - datetime(1899, 12, 30)
            start = float(delta.days) + (float(delta.seconds) / 86400)
        else:
             raise ValueError(f"У dateStart ожидался тип float или datetime а пришло {type(dateStart)}")
    else:
        start = np.min([np.min(frames[frame][dateName]) for frame in frames])

    # Определяем конец в датах
    if dateEnd is not None:
        if isinstance(dateEnd, float):
            end = dateEnd
        elif isinstance(dateEnd, datetime):
            delta = dateEnd - datetime(1899, 12, 30)
            end = float(delta.days) + (float(delta.seconds) / 86400)
        else:
            raise ValueError(f"У dateEnd ожидался тип float или datetime а пришло {type(dateEnd)}")
    else:
        end = np.max([np.max(frames[frame][dateName]) for frame in frames])

    print(f"dateStart = {start}")
    print(f"dateSnd = {end}")
    dates = np.arange(start, end, step)

    return dates


def dates_combine(frames, dateName):
    """
    Комбинирование дат

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dateName : str
        Какой заголовок считать датой
    """

    dfDates = pd.concat([frames[frame][dateName] for frame in frames]).drop_duplicates()
    dfDates.sort_values(inplace=True)
    dates = list(dfDates)

    return dates


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def convert_excel_to_dates(dates, strformat):
    """
    Подменяет список с числами-датами (excel) на список со строковыми или datetime-датами

    Parameters
    ----------
    dates : list, ndarray
        Список дат в числовом формате Excel
    strformat : str, optional
        В какой формат дат сохранить, если даты текстом.
        Если None, сохранит в datetime
    """

    base_date = datetime(1899, 12, 30)
    recovery = []
    for item in dates:
        dt = base_date + timedelta(days=item)
        if strformat is not None:
            dt = dt.strftime(strformat)
        recovery.append(dt)

    return recovery


def convert_dates_to_excel(frame, dateName, strformat):
    """
    Подменяет столбец со строковыми датами на столбец с числами-датами (excel)

    Parameters
    ----------
    frame : pd.DataFrame
        Фрейм с данными
    dateName : str
        Какой заголовок считать датой
    strformat : str
        Какой формат дат в данных, если даты текстом
    """

    base_date = datetime(1899, 12, 30)
    data = frame[dateName].tolist()

    # Конвертация строковых дат в число
    value = []
    for item in data:
        if isinstance(item, float) or isinstance(item, int):
            # Уже Excel-стиль, оставляем как есть
            dt_float = float(item)
        elif isinstance(item, datetime):
            # datetime -> float
            delta = item - base_date
            dt_float = float(delta.days) + (float(delta.seconds) / 86400)
        elif isinstance(item, str):
            # str -> datetime -> float
            try:
                dt = datetime.strptime(item, strformat)
            except ValueError:
                raise ValueError(f"Не удалось разобрать дату '{item}' с форматом '{strformat}'")
            delta = dt - base_date
            dt_float = float(delta.days) + (float(delta.seconds) / 86400)
        else:
            raise TypeError(f"Неподдерживаемый тип даты: {type(item)}")
        value.append(dt_float)

    frame.drop(dateName, axis=1, inplace=True)
    frame.insert(0, dateName, value)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def prepare_frames(filepath, dateName, strformat=None, data=None, sep=';', decimal=',') -> dict:
    """
    Подготавливает данные к интерполяции, при необходимости может читать файлы

    Данные можно передать двумя способами:
     1 - Напрямую, в виде pandas.Dataframe
     2 - Не напрямую, в виде пути к файлу формата .csv или .xlsx

    Метки времени предполагаются формата '%d.%m.%Y %H:%M' - '%d.%m.%Y %H:%M:%S:%f' и именем 'Дата Время'

    Parameters
    ----------
    filepath : str
        Путь расположения файла
    dateName : str
        Какой заголовок считать датой
    strformat : str, optional
        Какой формат дат в данных, если даты текстом
    data : pd.DataFrame, optional
        Датафрейм с данными
    sep : str, optional
        Разделитель данных для формата .csv
    decimal: str, optional
        десятичный разделитель для формата .csv
    """

    # Итоговые подготовленные к работе данные
    frames = {}

    # Если данные переданы напрямую
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    # Иначе, определяем формат и читаем
    elif filepath.endswith(".csv"):
        df = pd.read_csv(filepath, sep=sep, decimal=decimal)
    elif filepath.endswith(".xlsx"):
        df = pd.read_excel(filepath)
    else:
        print(f"Неподдерживаемый формат - {os.path.splitext(filepath)[1]}")
        return frames
    print(f"Прочитано - {filepath}")

    # Подготовка данных
    for col in df.columns:
        if col != dateName:
            frame = df[[dateName, col]].copy()
            frame.dropna(inplace=True)
            convert_dates_to_excel(frame, dateName, strformat)
            frame.sort_values(dateName, inplace=True)
            frame.reindex()
            frames[col] = frame

    return frames


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def main():

    filePath = "data/interpol/005-346_Luch_new 1m.csv"
    savePath = "result/interpol"
    dateName = "datetime"
    strformat = "%d.%m.%Y %H:%M:%S"  # "%Y-%m-%d %H:%M:%S"

    # тест прямой передачи
    test = {"datetime": [datetime(2025, 1, 1),datetime(2025, 2, 1),datetime(2025, 3, 1),datetime(2025, 4, 1)],
            "t1": [1,4,7,8], "t2": [2,5,1,6]}
    testdf = pd.DataFrame(test)

    # Чтение файлов
    frames = prepare_frames(filePath, dateName, strformat, sep=';', decimal='.')
    #frames = prepare_frames(filePath, dateName, strformat, data=testdf)

    # Интерполяция с генерацией дат
    #dates = dates_generation(frames, dateName, 1/24)
    #frames = frames_interpolation(frames, dates, dateName)

    # Исходные даты и значения
    #dates = dates_combine(frames, dateName)
    #frames = frames_combine(frames, dates)

    # Исходные даты и интерполяция
    dates = dates_combine(frames, dateName)
    frames = frames_interpolation(frames, dates, dateName)

    # Восстановить даты
    dates = convert_excel_to_dates(dates, strformat)
    #dates = convert_excel_to_dates(dates, None)

    # запись
    print(f'Запись в {savePath} ...')
    df = pd.DataFrame(frames)
    df.insert(0, dateName, dates)
    #df.to_csv(f"{savePath}.csv", encoding="utf-8", sep=';', index=False)
    df.to_excel(f"{savePath}.xlsx", index=False)
    print('Готово')


if __name__ == '__main__':
    main()
