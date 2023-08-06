from PIL import Image
import requests
import base64
from io import BytesIO
import io
def png_to_base64(image_url):
    """ Convert image url from database or from web to base64 """
    if image_url.startswith("http"):
        response = requests.get(image_url)
        file = open("sample_image.png", "wb")
        file.write(response.content)
        file.close()
        im = Image.open(file.name)
        buffer = io.BytesIO()
        im.save(buffer,format='PNG')
        byte_im = buffer.getvalue()
        base64qr = base64.b64encode(byte_im)
        img_data = base64qr.decode("utf-8")
        image_base64 = "data:image/png;base64, "+img_data
        return image_base64
    else:
        im = Image.open(image_url)
        buffer = io.BytesIO()
        im.save(buffer,format='PNG')
        byte_im = buffer.getvalue()
        base64qr = base64.b64encode(byte_im)
        img_data = base64qr.decode("utf-8")
        image_base64 = "data:image/png;base64, "+img_data
        return image_base64
