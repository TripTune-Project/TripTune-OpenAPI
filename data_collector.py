from api_handler import get_json_data
from db_handler import DatabaseHandler



def korea_city_code(db, secret_key, base_url):
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

    # 전체 갯수 조회s
    content = get_json_data(url, params)
    total_count = content["response"]["body"]["totalCount"]

    # DB 에 저장된 나라 id 조회
    select_country = "SELECT country_id FROM country WHERE country_name = '대한민국'"
    country_id = db.execute_select_one(select_country)[0]

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
            db.execute_insert(insert_city, (country_id, area_code, city_name))

    print("city 데이터 저장 완료")




def korea_district_code(db, secret_key, base_url):
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

    select_city = "SELECT city_id, api_area_code FROM city"
    cities = db.execute_select_all(select_city)
    

    for city in cities:
        city_id = city[0]
        params["areaCode"] = city[1]
        
        # 전체 갯수 조회
        content = get_json_data(url, params)
        total_count = content["response"]["body"]["totalCount"]

        pageNo = 0

        while pageNo * 10 < total_count:
            pageNo += 1
            params["pageNo"] = pageNo

            content = get_json_data(url, params)
            print(content)

            items = content["response"]["body"]["items"]["item"]

            for item in items:
                area_code = item["code"]
                district_name = item["name"]

                insert_district = "INSERT INTO district(city_id, api_area_code, district_name) VALUES (%s, %s, %s)"
                db.execute_insert(insert_district, (city_id, area_code, district_name))
        
    print("district 데이터 저장 완료")

