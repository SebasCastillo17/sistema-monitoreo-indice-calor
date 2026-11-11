from src.db.station.station_service import station_create
from src.imn_monitor.extraction.extract_station import get_stations
from src.imn_monitor.extraction.raw_data import raw_content

def upload_station():
    for station in get_stations(raw_content):
        station_create(name=station.name, active=station.active, name_region=station.region, location=station.location, url=station.url)
