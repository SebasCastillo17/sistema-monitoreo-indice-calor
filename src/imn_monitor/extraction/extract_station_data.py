import requests
from bs4 import BeautifulSoup

def get_station_data(url: str):
    request = requests.get(url)
    raw_data = BeautifulSoup(request.text)
    print(raw_data)

