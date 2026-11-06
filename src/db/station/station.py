from src.db.base import Base
from src.db.station_data.station_data import StationData

from typing import List
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Station(Base):
    __tablename__ = 'estacion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_region: Mapped[int] = mapped_column(Integer, ForeignKey("region.id"))
    nombre: Mapped[str] = mapped_column(String(512), unique=True)
    activa: Mapped[bool] = mapped_column(Boolean)
    ubicacion: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String)
    station: Mapped[List["StationData"]] = relationship()

