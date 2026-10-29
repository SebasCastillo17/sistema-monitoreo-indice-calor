from .region import Region
from src.db.session import session

def Create(name):
    try:
        region = Region(nombre=name)
        session.add(region)
        session.commit()
        return region

    except Exception as e:
        session.rollback()
        print(f"Error al crear la región '{name}'")
