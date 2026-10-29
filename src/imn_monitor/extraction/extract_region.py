import requests
from bs4 import BeautifulSoup
from src.imn_monitor.extraction.raw_data import raw_content

def get_regions(raw_region)->list:
    region = []

    # h2 is the region's title
    for r in raw_region.find_all('h2'):
        print(r.get_text())
        region.append(r.get_text())

    return region

