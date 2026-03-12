from abc import (
    ABC, abstractmethod,
)
from typing import (
    Dict, Any, Optional, final,
)
import requests
from PIL import Image 
from io import BytesIO
from utils.http_retry_adapter import _build_session
from interfaces.fuel_dict import FuelDict

class BaseStoreScraper(ABC):

    def __init__(self) -> None:
        self.session = _build_session()
    
    @abstractmethod
    def get_link(
        self, *args, **kwargs,
    ) -> str:
        pass 

    @final
    def get_img(self, url: str) -> Optional[bytes]:
        try:
            resp = self.session.get(url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException:
            return None
        try:
            image = Image.open(BytesIO(resp.content))
            image.thumbnail((64, 64))
            image = image.convert("L")
            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=40)
            return buffer.getvalue()
        except Exception:
            return None
    
    @abstractmethod
    def fetch(
        self, *args, **kwargs,
    ) -> Dict[str, Any]:
        pass 
    
    @abstractmethod
    def parse(
        self, *args, **kwargs,
    ) -> Any:
        pass

class BaseFuelScraper(ABC):
    def __init__(self) -> None:
        self.session = _build_session()

    @abstractmethod
    def parse(
        self, *args, **kwargs,
    ) -> FuelDict:
        pass