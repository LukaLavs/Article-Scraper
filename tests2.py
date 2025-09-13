import requests
from PIL import Image
from io import BytesIO

def get_img(url: str):
    image_resp = requests.get(url)
    try:
        image_resp.raise_for_status()
    except Exception:
        return None

    image = Image.open(BytesIO(image_resp.content))
    image.thumbnail((64, 64))
    #image = image.convert("L")
    
    # Preview image
    image.show()  # opens default image viewer

    # buffer = BytesIO()
    # image = image.convert("L")  # convert to grayscale
    # image.save(buffer, format="JPEG", quality=40)
    # image_bytes = buffer.getvalue()
    # return image_bytes

get_img('https://cdn1.interspar.at/cachableservlets/articleImage.dam/si/270241/dt_zoom.jpg')
