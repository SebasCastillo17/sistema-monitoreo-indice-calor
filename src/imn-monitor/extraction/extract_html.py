import requests
from bs4 import BeautifulSoup

URL = 'https://www.imn.ac.cr/web/imn/estaciones-automaticas'

r = requests.get(URL)

soup = BeautifulSoup(r.text, 'html.parser')

raw_content = soup.find_all('div', class_='journal-content-article')[1]

for station in raw_content.find_all('h2'):
    print(station.get_text())
