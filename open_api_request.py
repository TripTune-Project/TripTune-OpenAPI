import requests
import urllib
import os
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
base_url = os.getenv('BASE_URL')

params = {
    "serviceKey": secret_key,
    "numOfRows": 10,
    "pageNo": 1,
    "MobileOS": "ETC",
    "MobileApp": "AppTest",
    "_type": "json",
    "listYN": "Y",
    "arrange": "A",
    "contentTypeId": "32",
    "areaCode": "4",
    "sigunguCode": "4",
    "cat1": "B02",
    "cat2": "B0201",
    "cat3": "B02010100",
    "modifiedtime": "20220721"
}

params = urllib.parse.urlencode(params, safe='#\':()+=%,')

response = requests.get(base_url, params=params)
content = response.text

print(content)