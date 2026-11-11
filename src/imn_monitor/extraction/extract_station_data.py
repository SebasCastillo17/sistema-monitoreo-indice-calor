from datetime import datetime
from urllib.parse import urljoin
import re
import time

import requests
from bs4 import BeautifulSoup

imn_url = 'https://www.imn.ac.cr'

HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
    "User-Agent": "Mozilla/5.0",
}


class StationDataWeb:
    def __init__(self, date: datetime | None, tmax: float | None, temp: float | None, hr: float | None) -> None:
        self.date = date
        self.tmax = tmax
        self.temp = temp
        self.hr = hr


def clean_text(text: str) -> str:
    # Non-breaking spaces (\xa0, \u202f) -> regular space, then collapse whitespace
    text = text.replace('\xa0', ' ').replace('\u202f', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def cell_text(cell) -> str:
    # The HTML never closes its <td> tags, so html.parser nests them.
    # Take only the cell's own text, not the text of the nested "child" cells.
    return clean_text(''.join(cell.find_all(string=True, recursive=False)))


def get_table_values(raw_data: BeautifulSoup, required_columns: tuple[str, ...]) -> dict[str, str]:
    """Return {header: value} for the first data row of the first
    table that contains any of the required columns."""
    for table in raw_data.find_all('table'):
        rows = table.find_all('tr')
        if len(rows) < 2:
            continue

        headers = [clean_text(th.get_text()) for th in rows[0].find_all('th')]
        if not any(col in headers for col in required_columns):
            continue

        cells = [cell_text(td) for td in rows[1].find_all('td')]
        if len(cells) < len(headers):
            continue

        return dict(zip(headers, cells))

    return {}


def to_float(value: str | None) -> float | None:
    if not value:
        return None
    value = value.replace(' ', '')          # "1 005,57" -> "1005,57"
    if ',' in value:
        value = value.replace('.', '').replace(',', '.')  # "1.002,30" -> "1002.30"
    try:
        return float(value)
    except ValueError:
        return None


def to_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    # "p. m." / "p.m." / "p m" -> "PM"
    value = re.sub(r'\b([ap])\.?\s*m\.?', lambda m: m.group(1).upper() + 'M', value, flags=re.IGNORECASE)
    for fmt in ('%d/%m/%Y %I:%M:%S %p', '%d/%m/%Y %I:%M %p', '%d/%m/%Y %H:%M:%S'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def first_value(data: dict[str, str], *keys: str) -> str | None:
    for key in keys:
        if data.get(key):
            return data[key]
    return None


def parse_station(raw_data: BeautifulSoup, url: str) -> StationDataWeb | None:
    current_data = get_table_values(raw_data, ('Tmax',))
    average_data = get_table_values(raw_data, ('HR', 'RH'))

    date = to_datetime(current_data.get('Fecha'))
    tmax = to_float(current_data.get('Tmax'))
    temp = to_float(average_data.get('Temp'))
    hr = to_float(first_value(average_data, 'HR', 'RH'))

    if any(value is None for value in (date, tmax, temp, hr)):
        print(f'Station skipped: {url}, values reported: date: {date} tmax: {tmax} temp: {temp} hr: {hr}')
        return None

    return StationDataWeb(date, tmax, temp, hr)


def get_station_data(url: str) -> StationDataWeb | None:
    return parse_station(get_iframe_station(url), url)


def fetch(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, params={"_": str(time.time())}, timeout=30)
    response.raise_for_status()
    # Pass bytes (not response.text) so BeautifulSoup honors <meta charset="utf-8">.
    # With response.text, requests assumes ISO-8859-1 and "p.\xa0m." becomes "p.Â m."
    return BeautifulSoup(response.content, "html.parser")


def get_iframe_station(url: str) -> BeautifulSoup:
    soup = fetch(url)

    iframe = soup.find("iframe", id="datos")
    if iframe is None:
        raise ValueError(f"Iframe not found at {url}")

    iframe_src = iframe.get("src")
    if not isinstance(iframe_src, str):
        raise ValueError("The iframe does not have a valid URL")

    return fetch(urljoin(url, iframe_src))
