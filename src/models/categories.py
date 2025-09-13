from __future__ import annotations
from typing import (
    TYPE_CHECKING,
)
if TYPE_CHECKING: 
    from .articles import Article
from sqlalchemy import (
    ForeignKey, String,
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
)
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), index=True)
    category1: Mapped[str] = mapped_column(String)
    category2: Mapped[str] = mapped_column(String)
    category3: Mapped[str] = mapped_column(String)
    
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="category",
        uselist=False,
    )