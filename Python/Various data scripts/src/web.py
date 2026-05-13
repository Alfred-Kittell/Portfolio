# -*- coding: utf-8 -*-
"""
Парсер данных с сайта

(С) 2025 БО-Энерго,
"""
# ---- BUILT ----
import requests

# ---- OUTER ----
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


def main():
    """ """

    base_url = "https://all-pribors.ru/api/verification-results?rn=58953-14"

    # В Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Результаты поверки"
    headers = ["№", "заводской номер", "модификация", "результат поверки",
               "действительна до", "свидетельство о поверке", "дата поверки", "поверитель"]
    ws.append(headers)

    # номер строки
    num = 0

    for page in range(1, 24):
        if page > 1:
            url = f"{base_url}&page={page}"
        else:
            url = base_url

        print(f"Сбор данных с {url}")
        r = requests.get(url)
        data = r.json()
        docs = data.get("docs", [])
        if not docs:
            break
        all_docs = []
        all_docs.extend(docs)

        for i, d in enumerate(all_docs, start=1):
            num += 1
            ws.append([
                num,
                d.get("mi.number"),
                d.get("mi.modification"),
                d.get("result_text"),
                d.get("valid_date"),
                d.get("result_docnum"),
                d.get("verification_date"),
                d.get("org_title")
            ])

    wb.save("verification_results.xlsx")


def main2():
    """ """
    base_url = "https://all-pribors.ru/api/verification-results?rn=58953-14"
    all_docs = []

    for page in range(1, 24):
        url = f"{base_url}&page={page}"
        print(f"Сбор данных с {url}")
        r = requests.get(url)
        data = r.json()
        docs = data.get("docs", [])
        if not docs:
            break
        all_docs.extend(docs)

    # в DataFrame
    df = pd.DataFrame([{
        "№": i + 1,
        "заводской номер": d.get("mi.number"),
        "модификация": d.get("mi.modification"),
        "результат поверки": d.get("result_text"),
        "действительна до": d.get("valid_date"),
        "свидетельство о поверке": d.get("result_docnum"),
        "дата поверки": d.get("verification_date"),
        "поверитель": d.get("org_title")
    } for i, d in enumerate(all_docs)])

    # сохранить в Excel
    df.to_excel("verification_results.xlsx", index=False)

if __name__ == '__main__':
    main()
