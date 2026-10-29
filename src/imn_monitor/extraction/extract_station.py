from src.imn_monitor.extraction.raw_data import raw_content

def get_station(raw_content):
    for p in raw_content.find_all('table')[1].find_all('p'):
        print(p)
