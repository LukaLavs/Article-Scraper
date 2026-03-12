from typing import TypedDict
from decimal import Decimal

class FuelDict(TypedDict):
    type: str
    seller: str 
    price: Decimal 
    measure: str

