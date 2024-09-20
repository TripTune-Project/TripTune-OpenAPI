import os
import uuid
import datetime
from .data_collector_image import *
from api.api_handler import *
from utils.utils import *
from utils.log_handler import setup_logger
from db.db_handler import DatabaseHandler
from model.travel_place import TravelPlace
from model.location import Location
from aws import S3Handler


logger = setup_logger()

def korea_travel_places(db, s3, secret_key, base_url):
    '''
    DB에 저장되어 있는 지역 데이터(나라, 도시, 지역), 컨텐츠 타입을 이용해서 관광 정보를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.


    [Parameter]
    db: mysql 데이터베이스 연결
    s3: aws s3 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    '''
    url = base_url + '/areaBasedList1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    # 전체 지역 데이터 조회
    korea_areas = db.select_area_all()

    if not korea_areas:
        logger.error(f'지역 정보가 존재하지 않습니다 - {country}, {city}, {district}')
        return

    # 컨텐츠 타입 조회
    content_types = db.execute_select_all('SELECT * FROM api_content_type')


    for korea_area in korea_areas:
        location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])

        for content_type in content_types:
            params['contentTypeId'] = content_type['api_content_type_id']
            params['areaCode'] = korea_area['api_area_code']
            params['sigunguCode'] = korea_area['api_sigungu_code']

            total_count = get_total_count(url, params)

            if total_count != 0:
                items = fetch_items(url, params, total_count)

                for item in items:
                    travel_place = TravelPlace(
                        location,
                        item['cat3'],
                        content_type['content_type_id'],
                        item['title'],
                        item['addr1'],
                        item['addr2'] if item['addr2'] != '' else None,
                        item['mapx'],
                        item['mapy'],
                        item['contentid'],
                        convert_to_datetime(item['createdtime']),
                        convert_to_datetime(item['modifiedtime'])
                    )

                    db.insert_travel_place(travel_place)
                    place_id = db.execute_last_inserted_id()
                    
                     # 관광지 소개 정보 함수 호출
                    korea_travel_place_overview(db, secret_key, base_url, travel_place.api_content_id)

                    # 관광지 이미지 저장 함수 호출
                    if item['firstimage'] != '':
                        save_travel_image(db, s3, location.district_id, place_id, item['firstimage'], True)


        logger.info(f'{korea_area["city_name"]} 지역 {total_count}개 데이터 저장 완료')
    logger.info('korea_travel_places() - 관광지 데이터 저장 완료')



# 특정 지역 관광정보 조회 및 저장
def specific_korea_travel_places(db, s3, secret_key, base_url, country, city, district):
    '''
    파라미터로 전달된 지역 정보와 DB에 저장된 컨텐츠 타입을 이용해 특정 지역의 관광지를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.


    [Parameter]
    db: mysql 데이터베이스 연결
    s3: aws s3 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    country: 나라
    city: 도시
    district: 시군구
    '''
    url = base_url + '/areaBasedList1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    # 지역 조회
    korea_area = db.select_area_one(country, city, district)

    if not korea_area:
        logger.error(f'지역 정보가 존재하지 않습니다 - {country}, {city}, {district}')
        return

    # 컨텐츠 타입 조회
    content_types = db.execute_select_all('SELECT * FROM api_content_type')

    location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])

    for content_type in content_types:
        params['contentTypeId'] = content_type['api_content_type_id']
        params['areaCode'] = korea_area['api_area_code']
        params['sigunguCode'] = korea_area['api_sigungu_code']

        total_count = get_total_count(url, params)

        if total_count != 0:
            items = fetch_items(url, params, total_count)

            for item in items:
                travel_place = TravelPlace(
                        location,
                        item['cat3'],
                        content_type['content_type_id'],
                        item['title'],
                        item['addr1'],
                        item['addr2'] if item['addr2'] != '' else None,
                        item['mapx'],
                        item['mapy'],
                        item['contentid'],
                        convert_to_datetime(item['createdtime']),
                        convert_to_datetime(item['modifiedtime'])
                )

                db.insert_travel_place(travel_place)
                place_id = db.execute_last_inserted_id()

                # 관광지 소개 정보 함수 호출
                korea_travel_place_overview(db, secret_key, base_url, travel_place.api_content_id)

                # 관광지 이미지 저장 함수 호출
                if item['firstimage'] != '':
                    save_travel_image(db, s3, location.district_id, place_id, item['firstimage'], True)

        logger.info(f'{city} 지역 {total_count}개 데이터 저장 완료')
    logger.info('specific_korea_travel_places() - 관광지 데이터 저장 완료')


def limited_korea_travel_places(db, s3, secret_key, base_url, country, city, district):
    '''
    파라미터로 전달된 지역 정보와 DB에 저장된 컨텐츠 타입을 이용해 특정 지역의 관광지를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.

    *if문을 추가해 저장되는 데이터가 200개를 넘어가지 않게 설정했다.
    

    [Parameter]
    db: mysql 데이터베이스 연결
    s3: aws s3 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    country: 나라
    city: 도시
    district: 시군구
    '''
    url = base_url + '/areaBasedList1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    # 지역 조회
    korea_area = db.select_area_one(country, city, district)

    if not korea_area:
        logger.error(f'지역 정보가 존재하지 않습니다 - {country}, {city}, {district}')
        return


    # 컨텐츠 타입 조회
    content_types = db.execute_select_all('SELECT * FROM api_content_type')

    location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])

    # 총 갯수 확인하기 위한 변수
    count = 0

    for content_type in content_types:
        params['contentTypeId'] = content_type['api_content_type_id']
        params['areaCode'] = korea_area['api_area_code']
        params['sigunguCode'] = korea_area['api_sigungu_code']

        total_count = get_total_count(url, params)

        if total_count != 0 and count <= 200:
            items = fetch_items(url, params, total_count)

            for item in items:
                travel_place = TravelPlace(
                        location,
                        item['cat3'],
                        content_type['content_type_id'],
                        item['title'],
                        item['addr1'],
                        item['addr2'] if item['addr2'] != '' else None,
                        item['mapx'],
                        item['mapy'],
                        item['contentid'],
                        convert_to_datetime(item['createdtime']),
                        convert_to_datetime(item['modifiedtime'])
                    )

                db.insert_travel_place(travel_place)
                place_id = db.execute_last_inserted_id()

                # 관광지 소개 정보 함수 호출
                korea_travel_place_overview(db, secret_key, base_url, travel_place.api_content_id)

                # 관광지 이미지 저장 함수 호출
                if item['firstimage'] != '':
                    save_travel_image(db, s3, location.district_id, place_id, item['firstimage'], True)

                count += 1

        logger.info(f'{city} 지역 {count}개 데이터 저장 완료')
    logger.info('limited_korea_travel_places() - 관광지 데이터 저장 완료')



# 관광지 소개 정보 데이터 조회 및 저장
def korea_travel_place_overview(db, secret_key, base_url, api_content_id):
    '''
    파라미터로 전달된 관광지에 대한 소개 정보를 조회하고 저장한다.
    

    [Parameter]
    db: mysql 데이터베이스 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    api_content_id: open api에서 지정한 관광지 id
    '''
    url = base_url + '/detailCommon1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json',
        'overviewYN': 'Y'
    }

    params['contentId'] = api_content_id
    total_count = get_total_count(url, params)

    if total_count != 0:
        items = fetch_items(url, params, total_count)

        for item in items:
            if item['overview'] == '' or item['overview'] == '-':
                return None

            update_place_overview = 'UPDATE travel_place SET description = %s WHERE api_content_id = %s'
            db.execute_update(update_place_overview, (item['overview'], api_content_id))
                

    logger.info(f'korea_travel_place_overview() - 총 {total_count}개 관광지 설명 데이터 저장 완료')



