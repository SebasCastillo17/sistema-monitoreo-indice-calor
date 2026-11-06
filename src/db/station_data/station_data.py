from datetime import datetime

from src.db.base import Base
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped

class StationData(Base):
    __tablename__ = 'datos_estacion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_estacion: Mapped[int] = mapped_column(Integer, ForeignKey("estacion.id"))
    # TODO: change the name "fecha_creacion" for something more specific
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime)
    temp: Mapped[float] = mapped_column(Float)
    tmax: Mapped[float] = mapped_column(Float)
    hr: Mapped[float] = mapped_column(Float)




