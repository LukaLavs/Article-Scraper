from __future__ import annotations
from typing import (
    TYPE_CHECKING,
)
if TYPE_CHECKING: 
    from .articles import Article
from sqlalchemy import (
    ForeignKey, String, LargeBinary,
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship,
)
from .base import Base

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), index=True)
    image: Mapped[bytes] = mapped_column(LargeBinary)
    
    article: Mapped[Article] = relationship(
        "Article",
        back_populates="image",
        uselist=False,
    )