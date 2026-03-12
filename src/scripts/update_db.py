from scraping.scrape_mercator import MercatorScraper
from scraping.scrape_fuel_sellers import PetrolScraper
from fill_database.fill import UpdateDatabase
from sqlalchemy.orm import Session
from models import (
    Base,
)
from database_config.database import engine
from utils.logging import log

    
if __name__ == "__main__":
    """ Update the database with new products/prices """
    
    Base.metadata.create_all(engine)
    
    mercator_scraper = MercatorScraper()
    petrol_scraper = PetrolScraper()
    updater = UpdateDatabase()
    session = Session(engine) 
        
    if True: 
        updater.insert_fuel_prices(
            session=session,
            scraper=petrol_scraper,
        )
    # except Exception as e: 
    #     log.error(f"Petrol Scraper Failed!\n{e}")

    try: 
            
        updater.insert_mercator_articles(
            scraper=mercator_scraper,
            session=session,
            limit=100,
            offset=0,
            MAX_PRODUCTS=40_000,
        )
    except Exception as e: 
        log.error(f"Mercator Scraper Failed!\n{e}")

        