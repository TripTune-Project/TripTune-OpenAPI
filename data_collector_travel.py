from api_handler import *
from utils import *
from db_handler import DatabaseHandler


# 지역기반 관광정보 조회 및 저장
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
            params["contentTypeId"] = content_type["api_content_type_id"]
            params["areaCode"] = area_code
            params["sigunguCode"] = sigungu_code

            total_count = get_total_count(url, params)

            if total_count != 0:
                items = fetch_items(url, params, total_count)

                for item in items:
                    district_id = korea_area["district_id"]
                    category_code = item["cat3"]
                    content_type_id = content_type["content_type_id"]
                    place_name = item["title"]
                    address = item["addr1"]
                    detail_address = item["addr2"] if item["addr2"] != "" else None
                    longitude = item["mapx"]
                    latitude = item["mapy"]
                    api_created_at = convert_to_datetime(item["createdtime"])
                    api_updated_at = convert_to_datetime(item["modifiedtime"])
                    api_content_id = item["contentid"]

                    insert_travel_place = """INSERT INTO travel_place(district_id, category_code, content_type_id, place_name, address, detail_address
                                                , longitude, latitude, api_content_id, created_at, api_created_at, api_updated_at) 
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s)"""

                    db.execute_insert(insert_travel_place
                        , (district_id, category_code, content_type_id, place_name, address, detail_address, longitude, latitude, api_content_id, api_created_at, api_updated_at))
                    
                     # 관광지 소개 정보 함수 호출
                    korea_detail_common(db, secret_key, base_url, api_content_id)

        print("------------지역 기반 데이터 저장 사이클------------")

    print("***관광지 데이터 저장 완료***")


# 특정 지역 관광정보 조회 및 저장
def korea_specific_area_based_list(db, secret_key, base_url, city, district):
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
                                WHERE c.city_name = %s
                                AND d.district_name = %s
                                """
    korea_area = db.execute_select_one(select_city_and_district, (city, district))

    # 컨텐츠 타입 조회
    select_content_types = "SELECT * FROM api_content_type"
    content_types = db.execute_select_all(select_content_types)

    area_code = korea_area["api_area_code"]
    sigungu_code = korea_area["api_sigungu_code"]
    district_id = korea_area["district_id"]


    for content_type in content_types:
        params["contentTypeId"] = content_type["api_content_type_id"]
        params["areaCode"] = area_code
        params["sigunguCode"] = sigungu_code

        total_count = get_total_count(url, params)

        if total_count != 0:
            items = fetch_items(url, params, total_count)

            for item in items:
                category_code = item["cat3"]
                content_type_id = content_type["content_type_id"]
                place_name = item["title"]
                address = item["addr1"]
                detail_address = item["addr2"] if item["addr2"] != "" else None
                longitude = item["mapx"]
                latitude = item["mapy"]
                api_created_at = convert_to_datetime(item["createdtime"])
                api_updated_at = convert_to_datetime(item["modifiedtime"])
                api_content_id = item["contentid"]

                insert_travel_place = """INSERT INTO travel_place(district_id, category_code, content_type_id, place_name, address, detail_address
                                            , longitude, latitude, api_content_id, created_at, api_created_at, api_updated_at) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s)"""

                db.execute_insert(insert_travel_place
                    , (district_id, category_code, content_type_id, place_name, address, detail_address, longitude, latitude, api_content_id, api_created_at, api_updated_at))
                
                # 관광지 소개 정보 함수 호출
                korea_detail_common(db, secret_key, base_url, api_content_id)


    print("***관광지 데이터 저장 완료***")




# 특정 공통정보(관광지 소개 정보 데이터) 조회 및 저장
def korea_detail_common(db, secret_key, base_url, api_content_id):
    url = base_url + "/detailCommon1"

    params = {
        "serviceKey": secret_key,
        "numOfRows": 10,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "TripTune",
        "_type": "json",
        "overviewYN": "Y"
    }

    params["contentId"] = api_content_id
    total_count = get_total_count(url, params)

    if total_count != 0:
        items = fetch_items(url, params, total_count)

        for item in items:
            overview_value = item["overview"] if item["overview"] != "" else None

            update_place_overview = "UPDATE travel_place SET description = %s WHERE api_content_id = %s"
            db.execute_update(update_place_overview, (overview_value, api_content_id))
                

    print("***관광지 설명 데이터 저장 완료***")


