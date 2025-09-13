from scraping.scrape_mercator import MercatorScraper
from fill_database.fill import UpdateDatabase
from sqlalchemy.orm import Session
from models import (
    Base,
)
from database_config.database import engine

    
if __name__ == "__main__":
    """ Update the database with new products/prices """
    
    Base.metadata.create_all(engine)
    
    scraper = MercatorScraper()
    updater = UpdateDatabase()
    session = Session(engine) 
        
    updater.insert_mercator_articles(
        scraper=scraper,
        session=session,
        limit=100,
        MAX_PRODUCTS=10_000,
    )
        