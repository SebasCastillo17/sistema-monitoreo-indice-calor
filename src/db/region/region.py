from typing import List

from src.db.base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from src.db.station.station import Station

class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(128), unique=True)
    station: Mapped[List["Station"]] = relationship()
