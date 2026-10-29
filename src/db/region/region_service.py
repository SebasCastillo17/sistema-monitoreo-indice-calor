from .region import Region
from src.db.session import session

def region_create(name:str):
    try:
        region = session.query(Region).filter_by(nombre=name).first()
        if region:
            return None
        region = Region(nombre=name)
        session.add(region)
        session.commit()
        return region

    except Exception as e:
        session.rollback()
        print(f"Error al crear la región '{name}'")

def region_read(name:str):
    try:
        region = session.query(Region).filter_by(nombre=name).first()
        return region
    except Exception as e:
        print(f"Error, {name} not found")
