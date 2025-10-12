from __future__ import annotations
from typing import (
    TYPE_CHECKING,
)
if TYPE_CHECKING:
    from scraping.scrape_mercator import MercatorScraper
from models import (
    Store, Article, Price, Category, Image,
    PriceLatest,
)
from typing import (
    Optional, Tuple, List, 
    final
)
from interfaces.article_dict import ArticleDict
from datetime import datetime   
from sqlalchemy.orm import Session
from utils.logging import log


class UpdateDatabase:
    
    @final    
    def insert_article(
        self,
        session: Session, 
        article_data: ArticleDict, 
        store_name: str, 
        scraper: MercatorScraper,
        ) -> Optional[Article]:
        
        if not (
            store := (
            session.query(Store)
            .filter_by(name=store_name).first()
            )
        ):
            log.info(f"Adding a store = {store_name}")
            store = Store(name=store_name)
            session.add(store)
            session.flush()
            
        if not (
            article := (
                session.query(Article)
                .join(Article.store)
                .filter(
                    Article.ean_13==article_data["ean_13"], 
                    Store.name == store_name
                )
                .first()
            )
        ):
            if not (
                image := scraper.get_img(url=article_data["image_link"])
            ):
                log.warning(
                    f"Image not provided. Skipping article: "
                    f"{article_data["name"]}."
                )
                return None
            
            article = Article(
            ean_13=article_data["ean_13"],
            name=article_data["name"],
            brand_name=article_data["brand_name"],
            invoice_unit=article_data["invoice_unit"],
            invoice_unit_type=article_data["invoice_unit_type"],
            store=store,
            )
            log.info(
                f"Adding an article {article_data["name"]}."
            )
            article.category = Category(
                category1=article_data["category1"],
                category2=article_data["category2"],
                category3=article_data["category3"],
            )
            article.image = Image(
                image=image,
            )
            
        if (
            latest_price := session.query(PriceLatest)
            .filter_by(article_id=article.id)
            .first()
        ) and (
            latest_price.price == article_data["price"]
        ) and (
            latest_price.price_per_unit == article_data["price_per_unit"]
        ):
            log.info(
                f"Unchanged price for article: {article_data["name"]}."
            )
            return None
        else: 
            if not latest_price:
                latest_price = PriceLatest(article=article)
                session.add(latest_price)
            log.info(
                f"New prices for article: {article_data["name"]}."
            )
            latest_price.price = article_data["price"]
            latest_price.price_per_unit = article_data["price_per_unit"]
            latest_price.price_per_unit_base = article_data["price_per_unit_base"]
            latest_price.timestamp = article_data["scraped_at"]
            
            article.prices.append(
                Price(
                    price=article_data["price"],
                    price_per_unit=article_data["price_per_unit"],
                    price_per_unit_base=article_data["price_per_unit_base"],
                    timestamp=article_data["scraped_at"],
                )
            )
            
        session.add(article)
        session.commit()
        
        return article
    
    def insert_mercator_articles(
        self,
        scraper: MercatorScraper,
        session: Session,
        limit: int = 100,
        offset: int = 0,
        MAX_PRODUCTS: int = 1000000,
    ) -> None:    
        log.info(
            f"Called insert_mercator_articles("
            f"{scraper=}, {session=}, {limit=},"
            f"{offset=}, {MAX_PRODUCTS=}"
        )
        request_timestamp = int(datetime.now().timestamp() * 1000)
        seen_ean_13: set | str = set()
        limit = limit
        offset = 0
        
        article: Optional[Tuple[List[ArticleDict], set[str], bool]]
        while (
            (
                article := scraper.parse(
                    request_timestamp=request_timestamp,
                    seen_ean_13=seen_ean_13,
                    limit=limit, offset=offset,
                )
            ) is not None and (
                offset * limit < MAX_PRODUCTS
            )
        ):
            articles_data, seen_ean_13, all_seen = article
            if all_seen:
                log.info(
                    "All codes seen. Stopping insert_mercator_articles."
                )
                break
            for article_data in articles_data:
                self.insert_article(
                    session=session,
                    article_data=article_data,
                    store_name="Mercator",
                    scraper=scraper,
                ) 
            
            offset += 1
        
        return None
            
            

    
