import requests
from bs4 import BeautifulSoup
from .scrape_base import BaseFuelScraper
from interfaces.fuel_dict import FuelDict

class PetrolScraper(BaseFuelScraper):

    BASE_URL = "https://www.petrol.si/prodajna-mesta/2342-bs-ljubljana-ac-barje-sever-bencinski-servis"

    def parse(self) -> FuelDict:

        html = requests.get(self.BASE_URL).text
        soup = BeautifulSoup(html, "html.parser")

        data = []

        for item in soup.select(".fuel-sort-wrapper .location-detail__service-item"):
            fuel_type = item.select_one(".location-detail__service-item-text").get_text(strip=True)
            price_measure = item.select_one(".location-detail__service-item-price").get_text(strip=True)
            if price_measure.strip() == "": continue
            price, measure = tuple(price_measure.split(' '))
            price = float(price.replace(',', '.'))
            data.append({
                "type": fuel_type,
                "seller": "Petrol",
                "price": price,
                "measure": measure,
            })
        return data