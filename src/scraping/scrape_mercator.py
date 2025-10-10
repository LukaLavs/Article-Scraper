import requests
from datetime import (
    date, datetime,
)
from typing import (
    Dict, Any, List, Optional, Tuple
)
from .scrape_base import BaseScraper
from interfaces.article_dict import ArticleDict

class MercatorScraper(BaseScraper):
    
    BASE_URL =  "https://mercatoronline.si/products/browseProducts/getProducts"
    
    def get_link(
        self, limit: int, offset: int,
        timestamp: int, from_: int,
    ) -> str:
        return f"{self.BASE_URL}?limit={limit}&offset={offset}&from{from_}&_={timestamp}"
    
    def fetch(
        self, limit: int, offset: int,
        timestamp: int, from_: int,
    ) -> Any:
        url = self.get_link(limit, offset, from_, timestamp)
        articles = requests.get(url)
        articles.raise_for_status()
        return articles.json()
    
    def _extract_article(
        self, 
        article_json: Any,
        scraped_at: date,
        ) -> Optional[ArticleDict]:
        if (
            "data" not in article_json.keys() or
            "mainImageSrc" not in article_json.keys()
        ):
            return None
        
        article_data = article_json["data"]
    
        ean_13: str | None = next(
            (
                gtin["gtin"] 
                for gtin in article_data.get("gtins", []) 
                if len(gtin["gtin"]) == 13
            ), 
            None
        )
        if ean_13 is None:
            return None

        name: str = article_data["name"]
        brand_name: str = article_data["brand_name"]
        price: float = float(
            article_data["current_price"]
        )
        price_per_unit: float = float(
            article_data["price_per_unit"]
        )
        price_per_unit_base: str = article_data["price_per_unit_base"]
        unit_quantity = float(
            article_data["unit_quantity"]
        )
        invoice_unit: str = article_data["invoice_unit"]
        invoice_unit_type: int = int(article_data["invoice_unit_type"])
        
        image_link: str = article_json["mainImageSrc"]
        
        category1: str = article_data["category1"]
        category2: str = article_data["category2"]
        category3: str = article_data["category3"]

        return {
            "ean_13": ean_13,
            "name": name,
            "brand_name": brand_name,
            "price": price,
            "price_per_unit": price_per_unit, 
            "price_per_unit_base": price_per_unit_base,
            "unit_quantity": unit_quantity,
            "invoice_unit": invoice_unit,
            "invoice_unit_type": invoice_unit_type,
            "image_link": image_link,
            "category1": category1,
            "category2": category2,
            "category3": category3,
            "scraped_at": scraped_at,
        }
        
    
    def parse(
        self, request_timestamp: int,
        seen_ean_13: set,
        limit: int = 20, offset: int = 0,
    ) -> Optional[Tuple[List[ArticleDict], set[str], bool]]:
        today = date.today()
        from_ = offset * limit
        scraped_at: date = today
        articles: List[ArticleDict] = []

        if (
            article_jsons := self.fetch(
                limit, offset, request_timestamp, from_,
            ).get("products", None)
        ):    
            for article_json in article_jsons:
                
                article: Optional[ArticleDict] \
                    = self._extract_article(
                    article_json=article_json,
                    scraped_at=scraped_at,
                )
                if article is None:
                    continue
                
                if (ean_13 := article["ean_13"]) in seen_ean_13:
                    
                    all_seen = True
                    return articles, seen_ean_13, all_seen
                else:
                    seen_ean_13.add(ean_13)
                    
                articles.append(article)
        else: 
            return None

        all_seen = False
        return articles, seen_ean_13, all_seen
