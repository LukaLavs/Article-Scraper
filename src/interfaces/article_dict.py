from typing import TypedDict
from decimal import Decimal
from datetime import date

class ArticleDict(TypedDict):
    ean_13: str
    name: str 
    brand_name: str 
    price: Decimal 
    price_per_unit: Decimal 
    price_per_unit_base: str 
    unit_quantity: Decimal 
    invoice_unit: str 
    invoice_unit_type: int 
    image_link: str 
    category1: str 
    category2: str 
    category3: str 
    scraped_at: date
 