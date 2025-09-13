from typing import TypedDict
from datetime import date

class ArticleDict(TypedDict):
    ean_13: str
    name: str 
    brand_name: str 
    price: float 
    price_per_unit: float 
    price_per_unit_base: str 
    unit_quantity: float 
    invoice_unit: str 
    invoice_unit_type: int 
    image_link: str 
    category1: str 
    category2: str 
    category3: str 
    scraped_at: date
 