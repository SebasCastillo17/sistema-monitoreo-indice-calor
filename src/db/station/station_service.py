from .station import Station
from src.db.session import session
from src.db.region.region_service import region_read
from .station import Station

def station_create(name_region:str, active:bool, name:str, location:str, url:str):
    try:
        region = region_read(name_region)
        if region is None:
            return None
        region_id = region.id
        station = Station(id_region=region_id, nombre=name, activa=active, ubicacion=location, url=url)
        session.add(station)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error al crear la estacion '{name}' {e}")
