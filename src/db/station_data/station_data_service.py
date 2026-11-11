from src.db.station_data.station_data import StationData
from src.imn_monitor.extraction.extract_station_data import StationDataWeb
from src.db.session import session

def station_data_create(station_data: StationDataWeb, id_station: int):
    try:
        station_data_new = StationData(id_estacion=id_station, fecha_creacion=station_data.date, temp=station_data.temp, tmax=station_data.tmax, hr=station_data.hr)
        session.add(station_data_new)
        session.commit()
    
    except Exception as e:
        session.rollback()
        print(f"Error in the station_data from station id ='{id_station}' {e}")