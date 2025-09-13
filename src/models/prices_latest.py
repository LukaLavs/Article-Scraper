from __future__ import annotations
from typing import (
    TYPE_CHECKING,
)
if TYPE_CHECKING: 
    from .articles import Article
from datetime import date
from sqlalchemy import (
    ForeignKey, Date, Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
)
from .base import Base

class PriceLatest(Base):
    __tablename__ = "prices_latest"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), index=True)
    price: Mapped[int] = mapped_column(Numeric(7, 2), nullable=False)
    price_per_unit: Mapped[float] = mapped_column(Numeric(7, 2))
    price_per_unit_base: Mapped[str] = mapped_column(String(3))
    timestamp: Mapped[date] = mapped_column(Date, default=date.today)
    
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="price_latest",
        uselist=False,
    )