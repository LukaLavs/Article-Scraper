from sqlalchemy import (
    String, Numeric, Date,
)
from sqlalchemy.orm import (
    Mapped, mapped_column,
)
from datetime import datetime

from .base import Base
    
class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(100))
    seller: Mapped[str] = mapped_column(String(225))
    price: Mapped[float] = mapped_column(Numeric)
    measure: Mapped[str] = mapped_column(String(7))
    timestamp: Mapped[datetime] = mapped_column(Date, default=datetime.now)
