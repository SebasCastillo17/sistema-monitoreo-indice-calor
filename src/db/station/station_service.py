from typing import Sequence

from sqlalchemy import Row, select

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
        station = session.query(Station).filter_by(nombre=name).first()
        if station:
            return None
        station = Station(id_region=region_id, nombre=name, activa=active, ubicacion=location, url=url)
        session.add(station)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error al crear la estacion '{name}' {e}")

def station_read_url() -> Sequence[Row[int, str]]:
    result = session.execute(
            select(Station.id, Station.url)
            .where(Station.activa == True)
            )
    return result.all()
