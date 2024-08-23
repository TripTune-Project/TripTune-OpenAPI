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


def compress_and_save_image (image_url, file_path, quality):
    response = requests.get(image_url)
    
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        img.save(file_path, "JPEG", quality=quality)
        print(f"이미지 저장 완료")
    else:
        print(f"이미지 압축 및 다운 실패, 상태 코드 : {response.status_code}")
