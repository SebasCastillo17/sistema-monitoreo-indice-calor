from .region import Region
from src.db.session import session

def Create(name):
    region = Region(nombre=name)
    session.add(region)
    try:
        session.commit()
    except Exception:
        session.rollback()
        raise
