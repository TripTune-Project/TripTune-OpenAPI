import requests
import urllib
import os
import json
from dotenv import load_dotenv


def korea_city_code1(secret_key, base_url):
    suffix = "/areaCode1"
    url = base_url + suffix

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "areaCode": "",
        "_type": "json",
    }

    content = get_json_data(url, params)
    total_count = content["response"]["body"]['totalCount']
    pageNo = 0

    while pageNo * 10 < total_count:
        pageNo += 1
        params["pageNo"] = pageNo

        content = get_json_data(url, params)
        print(content)

    return total_count


def get_json_data(url, params):
    encoding_params = urllib.parse.urlencode(params, safe='#\':()+=%,')

    response = requests.get(url, params=encoding_params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"요청 실패: 상태코드 {response.status_code}")



def main():
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    if not secret_key or not base_url:
        print("환경 변수 불러오기 실패")
        return

    korea_city_code1(secret_key, base_url)




if __name__ == '__main__':
    main()







