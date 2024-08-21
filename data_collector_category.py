from api_handler import *
from utils import *
from db_handler import DatabaseHandler


# 대분류 카테고리(cat1) 조회 및 저장
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

    print("***카테고리(cat1) 데이터 저장 완료***")


# 중분류 카테고리(cat2) 조회 및 저장
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

    print("***카테고리(cat2) 데이터 저장 완료***")


# 소분류 카테고리(cat3) 조회 및 저장
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

    print("***카테고리(cat3) 데이터 저장 완료***")
