from __future__ import annotations
from typing import (
    List, TYPE_CHECKING,
)
if TYPE_CHECKING: 
    from .articles import Article
from sqlalchemy import (
    String, 
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
)
from .base import Base


class Store(Base):
    __tablename__ = "stores"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    
    articles: Mapped[List[Article]] = relationship(
        "Article",
        back_populates="store",
        cascade="all, delete-orphan",
    )
    