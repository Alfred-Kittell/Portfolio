
import os
from copy import deepcopy
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
#from statsmodels.tsa.filters.hp_filter import hpfilter
import matplotlib.pyplot as plt
import openpyxl
from subprocess import PIPE, Popen, run

from src.postgres import PostgresControl

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


def parse_obscure(fname, type='i', dateName='Дата Время'):
    """
    Функция для считывания данных нестандартного формата
     с разделителями разной длины

    :param fname: str
        - Путь к файлу.
    :return: pandas.DataFrame
    """

    # считывание данных
    lines = []
    with open(fname, 'r', encoding='cp1251') as file:
        lines = file.readlines()

    # получение имён столбцов
    data = {dateName: []}
    columns = []
    for item in lines[0].split(' '):
        if item != '':
            columns.append(item.replace('\n', ''))
            data[columns[-1]] = []

    # получение данных столбцов
    for line in lines[1:]:
        values = []
        for item in line.split(' '):
            if item != '':
                values.append(item.replace('\n', ''))
        level = 0
        if type == 'i':
            for item in values:
                item = item.replace('****', '')
                #if item.replace('.', '', 1).isdigit():
                #    item = item.replace('.', ',', 1)
                data[columns[level]].append(item)
                level += 1
        else:
            event = []
            for item in values:
                if level < 4:
                    data[columns[level]].append(item)
                    level += 1
                else:
                    event.append(item)
            if len(event) > 0:
                data[columns[level]].append(" ".join(event))

    # обработка дат
    for ind in range(len(data['дата'])):
        d = data['дата'][ind]
        t = data['время'][ind]
        correctdate = f"{d} {t}"
        data[dateName].append(correctdate)
    del data['дата']
    del data['время']
    del data['']

    # заполнение dataframe данными
    if type == 'i':
        df = pd.DataFrame()
        for key, value in data.items():
            df[key] = value
            if key != dateName:
                df[key] = pd.to_numeric(df[key])
    else:
        df = pd.DataFrame(data)

    return df


def parse_7hi(fname, startread, filtnames, dataString):
    """
    Функция для считывания данных формата .7hi

    :param fname: str
        - Путь к файлу.
    :param startread: int
        - Строка начало данных в файле (имена столбцов).
    :param filtnames: list [начальное имя, итоговое имя]
        - Имена столбцов которые необходиво взять.
        Начальное имя, то, которое указано для столбца в файле.
        Итоговое имя, то, которое необходимо иметь после считывания.
    :param dataString: pd.DataFrame
        - Дата в строке.
    :return: pandas.DataFrame
    """

    # считывание данных
    lines = []
    encode = 'UTF-8'
    #encode = 'cp1251'
    with open(fname, 'r', encoding=encode) as file:
        lines = file.readlines()

    # получение имён столбцов и дополнение недостающих
    columns = lines[startread].split(' ')
    values = []
    maxcol = 0
    for line in lines[startread + 1:]:
        buf = line.split(' ')
        maxcol = maxcol if maxcol > len(buf) else len(buf)
        values.append(buf)
    [columns.append(f"Неизвестно {i+1}") for i in range(maxcol - len(columns))]

    # заполнение буфера данными
    data = {item: [] for item in columns[4:]}
    data[dataString] = []
    for line in values:
        d = line[2]
        t = line[3]

        year = int("20" + d[0:2])
        month = int(d[2:4])
        day = int(d[4:])
        hour = int(t[0:2])
        minute = int(t[2:])
        second = 0

        try:
            #correctdate = f"{d[4:]}.{d[2:4]}.20{d[0:2]} {t[0:2]}:{t[2:]}:00"  # ДД.ММ.ГГГГ чч:мм:сс
            correctdate = datetime(year, month, day, hour, minute, second)
            data[dataString].append(correctdate)
        except:
            print(f"wrong date - {d} {t}")
            continue

        for colind in range(4, len(columns)):
            column = columns[colind]
            data[column].append(line[colind].replace(',', '.').replace('не\xa0число', ''))

    # заполнение dataframe данными
    df = pd.DataFrame()
    for ind in range(len(filtnames)):
        df.insert(ind, filtnames[ind][1], data[filtnames[ind][0]])
        last = df.columns[-1]
        if last != dataString:
            df[last] = pd.to_numeric(df[last])

    return df


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def dates_generation(frames: dict, dateName: str, step: float):
    """Генерация списка дат с шагом: 1/24 - 1 час, 1/48 - 30 минут, 1/17280 - 5 сек"""

    dateStart = np.min([np.min(frames[frame][dateName]) for frame in frames])
    dateEnd = np.max([np.max(frames[frame][dateName]) for frame in frames])
    # dateStart = 44593
    # dateEnd = 44773
    print(f"dateStart = {dateStart}")
    print(f"dateSnd = {dateEnd}")
    dates = np.arange(dateStart, dateEnd, step)

    return dates


def dates_combine(frames, dateName: str):
    """Комбинирование дат"""

    dfDates = pd.concat([frames[frame][dateName] for frame in frames]).drop_duplicates()
    dfDates.sort_values(inplace=True)
    dates = list(dfDates)

    return dates


def dates_read(path: str, dateName: str):
    """Считывание дат из файла"""

    df = pd.read_excel(path)
    df[dateName] = df[dateName].dt.strftime("%d.%m.%Y %H:%M:%S")
    convert_dates_to_excel(df, dateName, "%d.%m.%Y %H:%M:%S")

    return list(df[dateName])


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def frames_interpolation(frames, dates, dateName) -> dict:
    """
    Объединение фреймов с помощью интерполяции

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dates : list
        Список дат
    dateName : str
        Имя поля времени
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


def frames_combine(frames, dates, dateName) -> dict:
    """
    Объединение фреймов с сохранением исходных значений

    Parameters
    ----------
    frames : dict
        Фреймы с данными
    dates : list
        Список дат
    dateName : str
        Имя поля времени
    """

    # Подготовка
    data = {dt: None for dt in dates}

    # Заполнение
    for frame in frames:
        print(f"Combine - {frame}")
        _data = deepcopy(data)
        for dt, value in frames[frame].values:
            _data[dt] = value
        frames[frame] = _data.values()

    return frames


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def get_data_from_files(root, columnFilter, columns_7hi, dateName='Дата Время'):
    """
    Функция для чтения и объединения данных из файлов из .csv и .7hi
    Метки времени предполагаются формата '%d.%m.%Y %H:%M' - '%d.%m.%Y %H:%M:%S:%f' и именем 'Дата Время'

    :param root: str
        - Путь, по которому искать файлы.
    :param columnFilter: list
        - Фильтр имён столбцов с итоговыми именами.
    :param columns_7hi: list
        - Фильтр имён столбцов, для файлов .7hi.
    :return: dict
    """

    frames = {}

    for file in os.listdir(root):
        if not file.startswith("test") and not file.startswith("~$"):
            path = os.path.join(root, file)
            if file.endswith(".csv"):
                dt = pd.read_csv(path, sep=';', decimal=',')
            elif file.endswith(".xlsx"):
                dt = pd.read_excel(path)
            elif file.endswith(".7hi"):
                dt = parse_7hi(path, 1, columns_7hi, dateName)
            elif file.endswith(".I"):
                dt = parse_obscure(path, 'i', dateName)
            elif file.endswith(".A"):
                dt = parse_obscure(path, 'a', dateName)
            else:
                print(f"Pass - {path}")
                continue

            print(f"Read - {path}")
            # Все параметры из файла
            for dtCol in dt.columns:
                #col = dtCol.upper().replace('_', '').replace(' ', '')
                col = dtCol
                print(f'\tcolumns in file: {col}')

                # фильтрация и отделение столбцов (дата время; параметр)
                if columnFilter:
                    for filtCol in columnFilter:
                        if col == filtCol[0]:
                            dt2 = dt[[dateName, dtCol]]
                            dt2 = dt2.rename({dtCol: filtCol[1]}, axis=1)
                            if filtCol[1] in frames:
                                frames[filtCol[1]].append(dt2)
                            else:
                                frames[filtCol[1]] = [dt2]
                else:
                    if col != dateName:
                        dt2 = dt[[dateName, dtCol]]
                        dt2 = dt2.rename({dtCol: col}, axis=1)
                        if col in frames:
                            frames[col].append(dt2)
                        else:
                            frames[col] = [dt2]

            # Один файл, один параметр
            # col = os.path.splitext(os.path.basename(path))[0]
            # dt2 = dt[[dateName, 'Value']]
            # dt2 = dt2.rename({'Value': col}, axis=1)

            #if 'Частота сети' in col:
            #if 'ltc_pos' not in col:
            #    dt2 = dt2.replace(0, np.nan)

            if col in frames:
                frames[col].append(dt2)
            else:
                frames[col] = [dt2]

    # Конечное объединение всех кусков
    for frame in frames:
        print(f"Convert - {frame}")
        frames[frame] = pd.concat(frames[frame], ignore_index=True)
        frames[frame].dropna(inplace=True)
        convert_dates_to_excel(frames[frame], dateName, "%d.%m.%Y %H:%M:%S")
        #replacement_dateColumn(frames[frame], dateName, True, "%Y-%m-%d %H:%M:%S")
        #frames[frame][frame] = pd.to_numeric(frames[frame][frame])
        frames[frame].sort_values(dateName, inplace=True)
        frames[frame].reindex()

    return frames


def get_data_from_signals(dataPath, dateName, columns, defguid="none"):
    """ """

    print(f"Open - {dataPath}")
    data = pd.read_csv(dataPath, sep=',', decimal='.')
    #data = pd.read_csv(dataPath, sep=';', decimal=',')

    assets = {}
    num = 0

    # Обработка данных
    for values in data.values:
    #for guid, asset, substation, signal, name, timestamp, value in data.values:
        num += 1
        if num % 50000 == 1:
            print(f"Convert - {num}")

        # Берём нужные параметры из строки
        if "guid" in columns:
            guid = values[columns["guid"]]
        else:
            guid = defguid
        timestamp = values[columns["datetime"]]
        signal = values[columns["signal"]]
        value = values[columns["value"]]

        # Фильтр не концентраций
        filt = ["_lim", "status_", "diag_"]
        if any([f in signal for f in filt]):
            continue

        #dt = timestamp[: timestamp.rfind('.')]  # string, стирание микросекунд
        #dt = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %H:%M:%S")  # int
        dt = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")  # int
        #dt = timestamp

        # Создание нового трансформатора
        if guid not in assets:
            assets[guid] = {}

        # Создания нового сигнала
        if signal not in assets[guid]:
            assets[guid][signal] = {dateName: [], signal: []}

        assets[guid][signal][dateName].append(dt)
        assets[guid][signal][signal].append(value)

    # финальная сборка
    for guid in assets.items():
        frames = guid[1]
        for frame in frames:
            print(f"Convert - {frame}")
            frames[frame] = pd.DataFrame(frames[frame])
            frames[frame].dropna(inplace=True)
            convert_dates_to_excel(frames[frame], dateName, "%Y-%m-%d %H:%M:%S")
            frames[frame].sort_values(dateName, inplace=True)
            frames[frame].reindex()

    return assets


def get_data_from_dump(columns):
    """Получение данных с дампа postgres"""

    # Создание буферной базы
    #postgresMain = PostgresControl("postgres", "admin", "postgres")
    #postgresMain.connect()
    #postgresMain.createDB("Buf")

    # Подключение к буферной базе
    postgresBuf = PostgresControl("postgres", "admin", "buf")
    postgresBuf.connect()
    frames = postgresBuf.test(columns)

    for frame in frames:
        frames[frame] = pd.DataFrame(frames[frame])
        frames[frame].dropna(inplace=True)
        #convert_dates_to_excel(frames[frame], "datetime", "%Y-%m-%d %H:%M:%S")
        convert_dates_to_excel(frames[frame], "datetime", None)
        frames[frame].sort_values("datetime", inplace=True)
        frames[frame].reindex()

    #restore_table("localhost", "buf", "postgres", "admin", )

    # Удаление буферной базы
    #postgresMain.dropDB("Buf")

    return frames


def restore_table(host_name, database_name, user_name, database_password):

    path = "bin/postgres/16/pg_restore.exe"
    dumpPath = "data/dumps/dump-postgres-202312011308_pahra"
    #command = f'{path} -h {host_name} -d {database_name} -U {user_name} < {dumpPath}'
    command = f'{path} -d {database_name} -U {user_name} {dumpPath}'

    p = Popen(command, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #p = run(command, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    #print(p.stdout.read())
    #print(p.stdin.read())

    return p.communicate(f'{database_password}\n'.encode(), timeout=5)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def smudgeData(path, dateName, dates, ignores):

    df = pd.read_csv(path, sep=',', decimal='.')
    df.sort_values(dateName, inplace=True)

    dateEnd = parse_datetime(np.max(dates), excel_format=True)
    dateStart = dateEnd - 145.321

    smudgeDates = np.linspace(dateStart, dateEnd, len(df[dateName]))
    newDates = dates[-len(smudgeDates)*3:]

    for ind in range(len(newDates)):
        newDates[ind] = parse_datetime(newDates[ind], excel_format=True)

    frames = {dateName: newDates}
    for column in df.columns:
        if column not in ignores:
            frames[column] = np.interp(newDates, smudgeDates, df[column])

    return pd.DataFrame(frames)


def hl_envelopes(data, dt, dmin=1, dmax=1, split=False):
    """
    Input :
    data: 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax: int, optional, size of chunks, use this if the size of the input signal is too big
    split: bool, optional, if True, split the signal in half along its mean, might help to generate the envelope in some cases
    Output :
    lmin, lmax : high/low envelope idx of input signal s
    """

    # locals min
    lmin = (np.diff(np.sign(np.diff(data))) > 0).nonzero()[0] + 1
    # locals max
    lmax = (np.diff(np.sign(np.diff(data))) < 0).nonzero()[0] + 1

    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(data)
        # pre-sorting of locals min based on relative position with respect to s_mid
        lmin = lmin[data[lmin] < s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid
        lmax = lmax[data[lmax] > s_mid]

    # global max of dmax-chunks of locals max
    lmin = lmin[[i + np.argmin(data[lmin[i:i + dmin]]) for i in range(0, len(lmin), dmin)]]
    # global min of dmin-chunks of locals min
    lmax = lmax[[i + np.argmax(data[lmax[i:i + dmax]]) for i in range(0, len(lmax), dmax)]]

    return lmin, lmax
    #return data[lmax], dt[lmax]
