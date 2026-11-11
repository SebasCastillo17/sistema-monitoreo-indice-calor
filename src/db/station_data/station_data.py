from datetime import datetime
from src.db.base import Base
from sqlalchemy import DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped

class StationData(Base):
    __tablename__ = 'datos_estacion'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_estacion: Mapped[int] = mapped_column(Integer, ForeignKey("estacion.id"))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    temp: Mapped[float] = mapped_column(Float, nullable=False)
    tmax: Mapped[float] = mapped_column(Float, nullable=False)
    hr: Mapped[float] = mapped_column(Float, nullable=False)

