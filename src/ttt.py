from scraping.scrape_mercator import MercatorScraper

mercator_scraper = MercatorScraper()
articles = mercator_scraper.parse()         
print(articles)   
