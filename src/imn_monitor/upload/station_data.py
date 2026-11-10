from src.imn_monitor.extraction.extract_station_data import get_station_data
from src.db.station.station_service import station_read_url

def upload_station_data():
    stations = station_read_url()
    station_data = get_station_data(stations[0][1])

    if station_data is None:
        print("Station skipped: incomplete data")
        return
    print(stations[0][1])
    print(station_data.date, station_data.hr, station_data.temp, station_data.tmax)

