from api_handler import *
from db_handler import DatabaseHandler
from datetime import datetime


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

    # 부모 카테고리 조회
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

    # 부모 카테고리 조회
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
        


def korea_area_based_list(db, secret_key, base_url):
    url = base_url + "/areaBasedList1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json"
    }

    # 도시, 지역 조회
    select_city_and_district = """SELECT c.city_id, c.city_name, c.api_area_code, d.district_id, d.district_name, d.api_sigungu_code
                                FROM city c
                                JOIN district d
                                ON c.city_id = d.city_id
                                """
    korea_areas = db.execute_select_all(select_city_and_district)

    # 컨텐츠 타입 조회
    select_content_types = "SELECT * FROM api_content_type"
    content_types = db.execute_select_all(select_content_types)


    for korea_area in korea_areas:
        area_code = korea_area["api_area_code"]
        sigungu_code = korea_area["api_sigungu_code"]

        for content_type in content_types:
            params["contentTypeId"] = content_type["api_content_id"]
            params["areaCode"] = area_code
            params["sigunguCode"] = sigungu_code

            total_count = get_total_count(url, params)

            if total_count != 0:
                items = fetch_items(url, params, total_count)

                for item in items:
                    district_id = korea_area["district_id"]
                    category_code = item["cat3"]
                    place_name = item["title"]
                    address = item["addr1"]
                    detail_address = item["addr2"]
                    longitude = item["mapx"]
                    latitude = item["mapy"]
                    api_created_at = convert_to_datetime(item["createdtime"])
                    api_updated_at = convert_to_datetime(item["modifiedtime"])

                    insert_travel_place = """INSERT INTO travel_place(district_id, category_code, place_name, address, detail_address
                                                , longitude, latitude, created_at, api_created_at, api_updated_at) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, now(), %s, %s)"""

                    db.execute_insert(insert_travel_place, (district_id, category_code, place_name, address, detail_address, longitude, latitude, api_created_at, api_updated_at))
                    
    print("------------area cycle------------")



def convert_to_datetime(date_string):
    date_format = "%Y%m%d%H%M%S"
    date_object = datetime.strptime(date_string, date_format)

    mysql_date_format = date_object.strftime("%Y-%m-%d %H:%M:%S")

    return mysql_date_format