from __future__ import annotations
from typing import (
    List, TYPE_CHECKING,
)
if TYPE_CHECKING: 
    from .stores import Store
    from .prices import Price
    from .categories import Category
    from .images import Image
    from .prices_latest import PriceLatest
    
from sqlalchemy import (
    UniqueConstraint, ForeignKey, String, 
    Numeric,
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
)
from .base import Base
    
class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        UniqueConstraint(
            "name", "ean_13", "store_id", name="uix_article",
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    ean_13: Mapped[str] = mapped_column(String(13), unique=True)
    name: Mapped[str] = mapped_column(String(225))
    brand_name: Mapped[str] = mapped_column(String)
    invoice_unit: Mapped[str] = mapped_column(String(3))
    invoice_unit_type: Mapped[int] = mapped_column(Numeric(1, 0))
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), index=True)
    
    store: Mapped[Store] = relationship(
        "Store",
        back_populates="articles",
    )
    category: Mapped[Category] = relationship(
        "Category",
        back_populates="article",
        uselist=False,
        cascade="all, delete-orphan",
    )
    image: Mapped[Image] = relationship(
        "Image",
        back_populates="article",
        uselist=False,
        cascade="all, delete-orphan",
    )
    prices: Mapped[List[Price]] = relationship(
        "Price",
        back_populates="article",
        cascade="all, delete-orphan",
    )
    price_latest: Mapped[PriceLatest] = relationship(
        "PriceLatest",
        back_populates="article",
        uselist=False,
        cascade="all, delete-orphan",
    )