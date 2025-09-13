from scraping.scrape_mercator import MercatorScraper
from fill_database.fill import UpdateDatabase
from sqlalchemy.orm import Session
from models import (
    Base, Store, Article, Category,
    Price, PriceLatest,
)
from database_config.database import engine

    
if __name__ == "__main__":



    

    
    scraper = MercatorScraper()
    
    updater = UpdateDatabase()
    Base.metadata.drop_all(engine) # TODO: remove after tests (Deletes all tables)
    Base.metadata.create_all(engine)
    
    with Session(engine) as session:
        
            
        updater.insert_mercator_articles(
            scraper=scraper,
            session=session,
            limit=5,
            MAX_PRODUCTS=5
        )
        
        
    with Session(engine) as session:
        # Print all stores
        print("STORES:")
        for store in session.query(Store).all():
            print(store.id, store.name)
        
        # Print all articles
        print("\nARTICLES:")
        for article in session.query(Article).all():
            print(
                article.id,
                article.ean_13,
                article.name,
                article.brand_name,
                article.store.name
            )
        
        # Print categories
        print("\nCATEGORIES:")
        for category in session.query(Category).all():
            print(category.id, category.article_id, category.category1, category.category2, category.category3)
        
        # Print prices
        print("\nPRICES:")
        for price in session.query(Price).all():
            print(price.id, price.article_id, price.price, price.price_per_unit, price.timestamp)
        
        # Print latest prices
        print("\nLATEST PRICES:")
        for lp in session.query(PriceLatest).all():
            print(lp.id, lp.article_id, lp.price, lp.price_per_unit, lp.timestamp)
        
            
        
    