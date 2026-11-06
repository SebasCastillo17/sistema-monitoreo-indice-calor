from src.db.station.station_service import station_read_url

def upload_station_data():
    stations = station_read_url()
