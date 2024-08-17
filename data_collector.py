from api_handler import *
from db_handler import DatabaseHandler

'''
> 컨텐츠 타입 변수명
관광지: tourist
문화시설: cultural
축제공연행사: festival
여행코스: travel_course
레포츠: leports
숙박: accommodation
쇼핑: shopping
음식점: restaurants
'''

content_types = [{"tourist": "12"}, {"cultural": "14"}, {"festival": "15"}, {"travel_course": "25"}, {"leports": "28"}, 
{"accommodation": "32"}, {"shopping": "38"}, {"restaurants": "39"}]


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

        insert_category = "INSERT INTO api_category(category_code, category_name, level) VALUES (%s, %s, %s)"
        db.execute_insert(insert_category, (category_code, category_name, 1))

    print("카테고리(cat1) 데이터 저장 완료")



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

    # 부모 카데고리 조회
    select_category1 = "SELECT * FROM api_category WHERE LEVEL = 1"
    categoris = db.execute_select_all(select_category1)

    for category in categoris:
        cat1_code = category["category_code"]
        params["cat1"] = cat1_code

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)
        
        for item in items:
            category_code = item["code"]
            category_name = item["name"]

            insert_category = "INSERT INTO api_category(category_code, category_name, parent_code, level) VALUES (%s, %s, %s, %s)"
            db.execute_insert(insert_category, (category_code, category_name, parent_code, 2))

    print("카테고리(cat2) 데이터 저장 완료")



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

    # 부모 카데고리 조회
    select_category2 = "SELECT * FROM api_category WHERE LEVEL = 2"
    categoris = db.execute_select_all(select_category2)


    for category in categoris:
        cat2_code = category["category_code"]
        params["cat1"] = category["parent_code"]
        params["cat2"] = cat2_code

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)

        for item in items:
            category_code = item["code"]
            category_name = item["name"]

            insert_category = "INSERT INTO api_category(category_code, category_name, parent_code, level) VALUES (%s, %s, %s, %s)"
            db.execute_insert(insert_category, (category_code, category_name, cat2_code, 3))

    print("카테고리(cat3) 데이터 저장 완료")
        


    
