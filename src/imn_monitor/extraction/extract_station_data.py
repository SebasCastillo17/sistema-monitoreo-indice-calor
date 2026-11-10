from datetime import datetime, time
from urllib.parse import urljoin

import re
import requests
from bs4 import BeautifulSoup

imn_url = 'https://www.imn.ac.cr'

class StationData:
    def __init__(self, date:datetime | None, tmax:float | None, temp:float | None, hr:float | None) -> None:
        self.date = date
        self.tmax = tmax
        self.temp = temp
        self.hr = hr

def get_table_values(raw_data, required_column: str):
    for table in raw_data.find_all('table'):
        rows = table.find_all('tr')

        if len(rows) < 2:
            continue

        headers = [
            th.get_text(strip=True)
            for th in rows[0].find_all('th')
        ]

        if required_column not in headers:
            continue

        row_text = rows[1].get_text(" ", strip=True)

        date_match = re.search(
            r'\d{2}/\d{2}/\d{4}(?:\s+\d{2}:\d{2}:\d{2}\s+[ap]\.m\.)?',
            row_text,
            re.IGNORECASE
        )

        if not date_match:
            continue

        date = date_match.group()
        numbers = re.findall(
            r'-?\d+(?:[,.]\d+)?',
            row_text[date_match.end():]
        )

        if len(numbers) != len(headers) - 1:
            continue

        values = dict(zip(headers[1:], numbers))
        values['Fecha'] = date

        return values

    return {}


def get_station_data(url: str) -> StationData | None:
    raw_data = get_iframe_station(url)

    current_data = get_table_values(raw_data, 'Tmax')
    average_data = get_table_values(raw_data, 'Temp')

    def to_float(value):
        try:
            return float(value.replace(',', '.')) if value else None
        except (ValueError, AttributeError):
            return None

    def to_datetime(value):
        if not value:
            return None

        value = value.replace('p.m.', 'PM').replace('a.m.', 'AM')

        try:
            return datetime.strptime(value, '%d/%m/%Y %I:%M:%S %p')
        except ValueError:
            return None

    date = to_datetime(current_data.get('Fecha'))
    tmax = to_float(current_data.get('Tmax'))
    temp = to_float(average_data.get('Temp'))
    hr = to_float(average_data.get('HR'))

    if any(value is None for value in (date, tmax, temp, hr)):
        print(f'Station skipped: {url}')
        return None

    return StationData(date, tmax, temp, hr)
    

def get_iframe_station(url: str) -> BeautifulSoup:
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        params={"_": str(time())}
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    iframe = soup.find("iframe", id="datos")

    if iframe is None:
        raise ValueError(f"No se encontró el iframe en {url}")

    iframe_src = iframe.get("src")

    if not isinstance(iframe_src, str):
        raise ValueError("El iframe no tiene una URL válida")

    iframe_url = urljoin(url, iframe_src)

    response = requests.get(
        iframe_url,
        headers=headers,
        params={"_": str(time())}
    )
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")