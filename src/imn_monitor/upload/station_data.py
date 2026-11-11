from src.imn_monitor.extraction.extract_station_data import get_station_data
from src.db.station.station_service import station_read_url
from src.db.station_data.station_data_service import station_data_create

def upload_station_data():
    stations = station_read_url()

    for station_id, station_url in stations:
        try:
            station_data = get_station_data(station_url)

            if station_data is None:
                print(f'Station with id = {station_id}')
            else:
                station_data_create(station_data=station_data, id_station=station_id)
        except ValueError as e :
            print(f"ERROR:{e}")