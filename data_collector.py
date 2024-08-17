from api_handler import *
from db_handler import DatabaseHandler


def korea_city_code(db, secret_key, base_url):
    url = base_url + "/areaCode1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json",
    }

    # 전체 갯수 조회
    total_count = get_total_count(url, params)

    # DB 에 저장된 나라 id 조회
    select_country = "SELECT country_id FROM country WHERE country_name = '대한민국'"
    country_id = db.execute_select_one(select_country)["country_id"]

    items = fetch_items(url, params, total_count)

    for item in items:
        area_code = item["code"]
        city_name = item["name"]

        insert_city = "INSERT INTO city(country_id, api_area_code, city_name) VALUES (%s, %s, %s)"
        db.execute_insert(insert_city, (country_id, area_code, city_name))

    print("city 데이터 저장 완료")



def korea_district_code(db, secret_key, base_url):
    url = base_url + "/areaCode1"

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
        city_id = city["city_id"]
        params["areaCode"] = city["api_area_code"]
        
        # 전체 갯수 조회
        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)

        for item in items:
            sigungu_code = item["code"]
            district_name = item["name"]

            insert_district = "INSERT INTO district(city_id, api_sigungu_code, district_name) VALUES (%s, %s, %s)"
            db.execute_insert(insert_district, (city_id, sigungu_code, district_name))
        
    print("district 데이터 저장 완료")



def korea_category1_code(db, secret_key, base_url):
    url = base_url + "/categoryCode1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json"
    }

    total_count = get_total_count(url, params)
    items = fetch_items(url, params, total_count)

    for item in items:
        category_code = item["code"]
        category_name = item["name"]

        insert_large_category = "INSERT INTO api_large_category(api_cat1_code, large_category_name) VALUES (%s, %s)"
        db.execute_insert(insert_large_category, (category_code, category_name))

    print("대분류 카테고리(cat1) 데이터 저장 완료")



def korea_category2_code(db, secret_key, base_url):
    url = base_url + "/categoryCode1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json"
    }

    select_large_category = "SELECT * FROM api_large_category"
    large_categoris = db.execute_select_all(select_large_category)

    for category in large_categoris:
        large_category_id = category["large_category_id"]
        params["cat1"] = category["api_cat1_code"]

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)
        
        for item in items:
            category_code = item["code"]
            category_name = item["name"]

            insert_middle_category = "INSERT INTO api_middle_category(large_category_id, api_cat2_code, middle_category_name) VALUES (%s, %s, %s)"
            db.execute_insert(insert_middle_category, (large_category_id, category_code, category_name))

    print("중분류 카테고리(cat2) 데이터 저장 완료")



def korea_category3_code(db, secret_key, base_url):
    url = base_url + "/categoryCode1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json"
    }

    select_middle_category = '''SELECT amc.middle_category_id, amc.api_cat2_code, amc.large_category_id, alc.api_cat1_code
                                FROM api_middle_category amc
                                JOIN api_large_category alc
                                ON amc.large_category_id = alc.large_category_id'''

    middle_categories = db.execute_select_all(select_middle_category)


    for category in middle_categories:
        middle_category_id = category["middle_category_id"]
        params["cat1"] = category["api_cat1_code"]
        params["cat2"] = category["api_cat2_code"]

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)

        for item in items:
            category_code = item["code"]
            category_name = item["name"]

            insert_small_category = "INSERT INTO api_small_category(middle_category_id, api_cat3_code, small_category_name) VALUES (%s, %s, %s)"
            db.execute_insert(insert_small_category, (middle_category_id, category_code, category_name))

    print("중분류 카테고리(cat3) 데이터 저장 완료")
        


    
