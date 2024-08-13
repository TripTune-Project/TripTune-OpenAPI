import requests
import urllib
import os
import json
import pymysql
from dotenv import load_dotenv


conn = None
cursor = None

def korea_city_code(secret_key, base_url):
    suffix = "/areaCode1"
    url = base_url + suffix

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json",
    }

    # 전체 갯수 조회
    content = get_json_data(url, params)
    total_count = content["response"]["body"]["totalCount"]

    # DB 에 저장된 나라 id 조회
    select_country = "SELECT country_id FROM country WHERE country_name = '대한민국'"
    cursor.execute(select_country)
    country_id = cursor.fetchone()[0]

    pageNo = 0

    while pageNo * 10 < total_count:
        pageNo += 1
        params["pageNo"] = pageNo

        content = get_json_data(url, params)
        print(content)

        items = content["response"]["body"]["items"]["item"]

        for item in items:
            area_code = item["code"]
            city_name = item["name"]

            insert_city = "INSERT INTO city(country_id, api_area_code, city_name) VALUES (%s, %s, %s)"
            cursor.execute(insert_city, (country_id, area_code, city_name))

    print("city 데이터 저장 완료")
    conn.commit()

    

def get_json_data(url, params):
    # parameter 인코딩 후 데이터 요청
    encoding_params = urllib.parse.urlencode(params, safe='#\':()+=%,')

    response = requests.get(url, params=encoding_params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"요청 실패: 상태코드 {response.status_code}")
        return


def main():
    global conn
    global cursor

    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = int(os.getenv("DB_PORT"))

    if not all([secret_key, base_url, db_host, db_user, db_password, db_name, db_port]):
        print("환경 변수 불러오기 실패")
        return

    conn = pymysql.connect(
        host=db_host, 
        user=db_user, 
        password=db_password, 
        db=db_name, 
        port=db_port, 
        charset="utf8"
    )

    cursor = conn.cursor()

    korea_city_code(secret_key, base_url)
   
    conn.close()



if __name__ == '__main__':
    main()







