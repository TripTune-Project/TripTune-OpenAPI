from api_handler import *
from db_handler import DatabaseHandler
from datetime import datetime


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
    korea_area = db.execute_select_all(select_city_and_district, (city, district))

    print(korea_area)

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
                

    print("***관광지 데이터 저장 완료***")
    print("***korea_specific_detail_common 요청***")
    korea_specific_area_based_list(db, secret_key, base_url, district_id)



# 특정공통정보(관광지 소개 정보 데이터) 조회 및 저장
def korea_specific_detail_common(db, secret_key, base_url, district_id):
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

    select_content_id = "SELECT api_content_id FROM travel_place WHERE district_id = %s"
    content_ids = db.execute_select_all(select_content_id, district_id)

    for content_id in content_ids:
        params["contentId"] = content_id["api_content_id"]
        total_count = get_total_count(url, params)

        if total_count != 0:
            items = fetch_items(url, params, total_count)

            for item in items:
                overview_value = item["overview"] if item["overview"] != "" else None

                update_place_overview = "UPDATE travel_place SET description = %s WHERE api_content_id = %s"
                db.execute_update(update_place_overview, (overview_value, content_id["api_content_id"]))
                

    print("***관광지 설명 데이터 저장 완료***")
    

    


def convert_to_datetime(date_string):
    date_format = "%Y%m%d%H%M%S"
    date_object = datetime.strptime(date_string, date_format)

    mysql_date_format = date_object.strftime("%Y-%m-%d %H:%M:%S")

    return mysql_date_format