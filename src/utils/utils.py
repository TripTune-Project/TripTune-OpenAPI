import os
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO


def convert_to_datetime(date_string):
    date_format = "%Y%m%d%H%M%S"
    date_object = datetime.strptime(date_string, date_format)

    mysql_date_format = date_object.strftime("%Y-%m-%d %H:%M:%S")

    return mysql_date_format


def download_and_compress_image(image_url, quality):
    response = requests.get(image_url)
    
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        img_byte_arr = BytesIO()
        img.save(img_byte_arr, "JPEG", quality=quality)

        img_byte_arr.seek(0)
        img_size = len(img_byte_arr.getvalue())

        print(f"***이미지 다운 및 압축 완료***")

        return img_byte_arr, img_size
    else:
        print(f"이미지 다운 및 압축 실패, 상태 코드 : {response.status_code}")
