from abc import (
    ABC, abstractmethod,
)
from typing import (
    Dict, Any, Optional, final,
)
import requests
from PIL import Image 
from io import BytesIO

class BaseScraper(ABC):
    
    @abstractmethod
    def get_link(
        self, *args, **kwargs,
    ) -> str:
        pass 

    @final
    def get_img(
        self, url: str,
    ) -> Optional[bytes]:
        image_resp = requests.get(url)
        try: 
            image_resp.raise_for_status()
        except Exception:
            return None
        image = Image.open(BytesIO(image_resp.content))
        image.thumbnail((64, 64))
        buffer = BytesIO()
        image = image.convert("L")
        image.save(buffer, format="JPEG", quality=40)
        image_bytes = buffer.getvalue()
        return image_bytes
    
    @abstractmethod
    def fetch(
        self, *args, **kwargs,
    ) -> Dict[str, Any]:
        pass 
    
    @abstractmethod
    def parse(
        self, *args, **kwargs,
    ) -> Dict[str, Any]:
        pass