from typing import (
    List, Tuple, Optional,
)
from sqlalchemy import (
    UniqueConstraint, Index, ForeignKey, String, Numeric, Date,
    select, tuple_,
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship,
)
from database import engine
from sqlalchemy.orm import Session
from datetime import date

class Base(DeclarativeBase):
    pass 

class Store(Base):
    __tablename__ = "stores"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    
    articles: Mapped[List["Article"]] = relationship(
        "Article",
        back_populates="store",
        cascade="all, delete-orphan",
    )
    
class Article(Base):
    __tablename__ = "articles"
    __table_args__ = (
        UniqueConstraint(
            "name", "ean_13", "store_code", "store_id", name="uix_article",
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    ean_13: Mapped[str] = mapped_column(String(13), unique=True)
    store_code: Mapped[str] = mapped_column(String(20))
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"), index=True)
    
    store: Mapped["Store"] = relationship(
        "Store",
        back_populates="articles",
    )
    
    prices: Mapped[List["Price"]] = relationship(
        "Price",
        back_populates="article",
        cascade="all, delete-orphan",
    )
    
class Price(Base):
    __tablename__ = "prices"
    __table_args__ = (
        Index(
            "ix_price_price_ts", 
            "article_id", "timestamp",
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"))
    price: Mapped[int] = mapped_column(Numeric(7, 2), nullable=False)
    timestamp: Mapped[date] = mapped_column(Date, default=date.today)
    
    article: Mapped["Article"] = relationship(
        "Article",
        back_populates="prices",
    )
    
def add_articles_to_store(
    session: Session,
    store_name: str,
    article_params: List[Tuple[str, Optional[str], Optional[str]]],
) -> List[Article]:
    # TODO: Check correctness (ean_13 has unique constraint, here it is not checked)
    store = (
        session.query(Store).filter(Store.name == store_name).first()
    )
    if store is None:
        raise ValueError(f"Store {store_name} not found.")

    existing_articles_query = (
        select(Article.name, Article.ean_13, Article.store_code)
        .where(
            Article.store_id == store.id, 
            (
                tuple_(Article.name, Article.ean_13, Article.store_code)
                .in_(article_params)
            )   
        )
    )
    existing_articles = set(session.execute(existing_articles_query).all())
    new_articles_params = [
        (name, ean_13, store_code) 
        for (name, ean_13, store_code) in article_params 
        if (name, ean_13, store_code) not in existing_articles
    ]
    new_articles = [
        Article(name=article_name, ean_13=ean_13, store_code=store_code, store=store) 
        for article_name, ean_13, store_code in new_articles_params
    ]
    if new_articles:
        session.add_all(new_articles)
        
    return new_articles
    
    
Base.metadata.create_all(engine)

# 2️⃣ Odpri sejo in dodaj sintetične podatke
with Session(engine) as session:
    # Dodamo nekaj trgovin
    store1 = Store(name="Lidl")
    store2 = Store(name="Tesco")
    session.add_all([store1, store2])
    session.commit()  # commit, da dobimo id-je

    # Dodamo nekaj artiklov
    articles_to_add = [
        ("Milk", "1234567890123", "M1"),
        ("Bread", "9876543210987", "B1"),
        ("Cheese", "1111111111111", "C1"),
        ("Milk", "1234567890124", "M2"),  # drug EAN
    ]

    # Uporabimo funkcijo add_articles_to_store
    new_articles = add_articles_to_store(session, "Lidl", articles_to_add)
    print(f"Added {len(new_articles)} articles to Lidl:")
    for a in new_articles:
        print(f"- {a.name}, {a.ean_13}, {a.store_code}")

    # Dodamo nekaj cen za te artikle
    prices_to_add = [
        Price(article=new_articles[0], price=1.99, timestamp=date.today()),
        Price(article=new_articles[1], price=0.99, timestamp=date.today()),
        Price(article=new_articles[2], price=2.49, timestamp=date.today()),
    ]
    session.add_all(prices_to_add)
    session.commit()

    # Preverimo, kaj je v bazi
    all_articles = session.query(Article).all()
    print("\nAll articles in the database:")
    for art in all_articles:
        print(f"{art.name}, {art.ean_13}, {art.store_code}, store={art.store.name}")

# Base.metadata.create_all(engine)
    
# with Session(engine) as session:
    
#     mercator = Store(
#         name="Mercator"
#     )
    
#     pepsi = Article(
#         name="Pepsi",
#         store=mercator
#     )
    
#     cocacola = Article(
#         name="Coca-Cola",
#         store=mercator
#     )
    
#     session.add(mercator)
#     session.commit()
    
#     print(list(a.name for a in mercator.articles))
