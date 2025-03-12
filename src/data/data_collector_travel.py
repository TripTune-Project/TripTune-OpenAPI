import os
import uuid
import datetime
from .data_collector_image import *
from api.api_handler import *
from utils.utils import *
from utils.log_handler import setup_logger
from utils.config import *
from db.db_handler import DatabaseHandler
from model.travel_place import TravelPlace
from model.location import Location
from aws import S3Handler


logger = setup_logger()

def korea_travel_places(db, s3):
    '''
    DB에 저장되어 있는 지역 데이터(나라, 도시, 지역), 컨텐츠 타입을 이용해서 관광 정보를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.
    저장 위치: travel_place

    '''
    url = BASE_URL + '/areaBasedList1'
    params = build_params()

    # 전체 지역 데이터 조회
    korea_areas = db.select_area_all()

    if not korea_areas:
        logger.error(f'지역 정보가 존재하지 않습니다')
        return

    # 컨텐츠 타입 조회
    content_types = db.execute_select_all('SELECT * FROM api_content_type')

    # 총 저장된 데이터 갯수 확인하기 위한 변수
    count = 0

    for korea_area in korea_areas:
        location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])

        for content_type in content_types:
            params['contentTypeId'] = content_type['api_content_type_id']
            params['areaCode'] = korea_area['api_area_code']
            params['sigunguCode'] = korea_area['api_sigungu_code']

            total_count = get_total_count(url, params)

            if total_count != 0:
                count = save_travel_places(db, s3, url, params, total_count, location, content_type, count)

        logger.info(f'{korea_area["city_name"]} 지역 {total_count}개 데이터 저장 완료')
    logger.info(f'korea_travel_places() - 관광지 {count}개 데이터 저장 완료')



# 특정 지역 관광정보 조회 및 저장
def specific_korea_travel_places(db, s3, city, district):
    '''
    파라미터로 전달된 지역 정보와 DB에 저장된 컨텐츠 타입을 이용해 특정 지역의 관광지를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.
    저장 위치: travel_place

    '''
    url = BASE_URL + '/areaBasedList1'
    params = params = build_params()

    # 지역 조회
    korea_area = db.select_area_one('대한민국', city, district)

    if not korea_area:
        logger.error(f'지역 정보가 존재하지 않습니다 - {city}, {district}')
        return

    # 컨텐츠 타입 조회
    content_types = db.execute_select_all('SELECT * FROM api_content_type')

    location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])

    # 총 저장된 데이터 갯수 확인하기 위한 변수
    count = 0

    for content_type in content_types:
        params['contentTypeId'] = content_type['api_content_type_id']
        params['areaCode'] = korea_area['api_area_code']
        params['sigunguCode'] = korea_area['api_sigungu_code']

        total_count = get_total_count(url, params)

        if total_count != 0:
            count = save_travel_places(db, s3, url, params, total_count, location, content_type, count)
                
        logger.info(f'{city} 지역 {total_count}개 데이터 저장 완료')
    logger.info(f'specific_korea_travel_places() - 관광지 {count}개 데이터 저장 완료')


def limited_korea_travel_places(db, s3, city, district, target_content_name, target_count):
    '''
    파라미터로 전달된 지역 정보와 DB에 저장된 컨텐츠 타입을 이용해 특정 지역의 관광지를 조회하고 저장한다.
    관광지 정보, 해당 관광지에 대한 소개 정보, 썸네일 이미지 등을 저장하는 기능을 한다.
    이미지 파일의 경우 S3에 이미지 파일로 저장된다.
    저장 위치: travel_place

    *if문을 추가해 저장되는 데이터 갯수를 제한했다.
    
    '''
    url = BASE_URL + '/areaBasedList1'
    params = build_params()


    # 지역 조회
    korea_area = db.select_area_one('대한민국', city, district)

    if not korea_area:
        logger.error(f'지역 정보가 존재하지 않습니다 - {city}, {district}')
        return


    # 컨텐츠 타입 조회
    content_type = db.execute_select_one('SELECT * FROM api_content_type WHERE content_type_name = %s', target_content_name)

    location = Location(korea_area['country_id'], korea_area['city_id'], korea_area['district_id'])
    

    # 총 저장된 데이터 갯수 확인하기 위한 변수
    count = 0

    params['contentTypeId'] = content_type['api_content_type_id']
    params['areaCode'] = korea_area['api_area_code']
    params['sigunguCode'] = korea_area['api_sigungu_code']

    total_count = get_total_count(url, params)
    logger.info(f'총 데이터 갯수(total_count) - {total_count} 개')

    if total_count != 0 and count <= target_count:
        count = save_travel_places(db, s3, url, params, total_count, location, content_type, count)
        
    logger.info(f'{city} 지역 {total_count}개 데이터 저장 완료')
    logger.info(f'limited_korea_travel_places() - 관광지 {count}개 데이터 저장 완료')



def save_travel_places(db, s3, url, params, total_count, location, content_type, count):
    items = fetch_items(url, params, total_count)

    for item in items:
        if not db.execute_exist_travel_place(item['contentid']):
            
            # 관광지 소개 정보 함수 호출
            details = korea_travel_place_detail(item['contentid'])

            # 관광지 기본 정보 함수 호출
            info = korea_travel_place_info(content_type['api_content_type_id'], item['contentid'])
    
            travel_place = TravelPlace(
                location=location,
                category_code=item['cat3'],
                content_type_id=content_type['content_type_id'],
                place_name=item['title'],
                address=item['addr1'],
                api_content_id=item['contentid'],
                api_created_at=convert_to_datetime(item['createdtime']),
                api_updated_at=convert_to_datetime(item['modifiedtime']),
                detail_address=item['addr2'] if item['addr2'] != '' else None,
                use_time=info['use_time'],
                check_in_time=info['check_in_time'],
                check_out_time=info['check_out_time'],
                homepage=details['homepage'],
                phone_number=info['phone_number'],
                longitude=item['mapx'],
                latitude=item['mapy'],
                description=details['description']
            )

            db.insert_travel_place(travel_place)
            place_id = db.execute_last_inserted_id()


            # 관광지 썸네일 이미지 저장 함수 호출
            if item['firstimage'] != '':
                save_travel_image(db, s3, location.district_id, place_id, item['firstimage'], True)

            # 관광지 이미지 저장 함수 호출
            limited_korea_travel_detail_image(db, s3, travel_place.api_content_id)
            count += 1
    
    return count



def korea_travel_place_detail(api_content_id):
    '''
    특정 관광지에 대한 소개 정보(description)와 홈페이지 정보(<a> 태그로 시작하는 홈페이지 주소)를 조회하고 저장한다.
    저장 위치 : travel_place.description

    '''
    url = BASE_URL + '/detailCommon1'
    params = build_detail_params()

    params['contentId'] = api_content_id
    total_count = get_total_count(url, params)

    if total_count != 0:
        items = fetch_items(url, params, total_count)

        for item in items:
            details = {
                'description': None, 
                'homepage': None
            }

            if item['overview'] != '' or item['overview'] != '-':
                details['description'] = item['overview']

            if item['homepage'] != '' or item['homepage'] != '-':
                start_index = item['homepage'].find('<a ')

                if start_index != -1:
                    details['homepage'] = item['homepage'][start_index:]
        
        logger.info(f'korea_travel_place_detail() - {api_content_id} 관광지 설명 데이터 조회 완료')
        return details

                

def korea_travel_place_info(api_content_type_id, api_content_id):
    '''
    콘텐츠 타입에 따른 관광지 정보(전화번호, 이용시간, 체크인 시간, 체크아웃 시간)를 조회한다.
    저장 위치 : travel_place.phone_number, travel_place.use_time, travel_place.check_in_time, travel_place.check_out_time

    '''

    url = BASE_URL + '/detailIntro1'
    params = build_params()

    params['contentId'] = api_content_id
    params['contentTypeId'] = api_content_type_id

    total_count = get_total_count(url, params)

    if total_count != 0:
        items = fetch_items(url, params, total_count)

        for item in items:
            info = {
                'phone_number': None,
                'use_time': None,
                'check_in_time': None,
                'check_out_time': None
            }

            if api_content_type_id == 12:   # 관광지
                info['phone_number'] = item['infocenter'] if item['infocenter'] != '' else None
                info['use_time'] = item['usetime'] if item['usetime'] != '' else None
            elif api_content_type_id == 14: # 문화시설
                info['phone_number'] = item['infocenterculture'] if item['infocenterculture'] != '' else None
                info['use_time'] = item['usetimeculture'] if item['usetimeculture'] != '' else None 
            elif api_content_type_id == 28: # 레포츠
                info['phone_number'] = item['infocenterleports'] if item['infocenterleports'] != '' else None
                info['use_time'] = item['usetimeleports'] if item['usetimeleports'] != '' else None 
            elif api_content_type_id == 32: # 숙박
                info['phone_number'] = item['infocenterlodging'] if item['infocenterlodging'] != '' else None
                info['check_in_time'] = item['checkintime'] if item['checkintime'] != '' else None
                info['check_out_time'] = item['checkouttime'] if item['checkouttime'] != '' else None
            elif api_content_type_id == 38: # 쇼핑      
                info['phone_number'] = item['infocentershopping'] if item['infocentershopping'] != '' else None
                info['use_time'] = item['opentime'] if item['opentime'] != '' else None 
            elif api_content_type_id == 39: # 음식점
                info['phone_number'] = item['infocenterfood'] if item['infocenterfood'] != '' else None
                info['use_time'] = item['opentimefood'] if item['opentimefood'] != '' else None 
   

        logger.info(f'korea_travel_place_info() - {api_content_id} 관광지 전화번호, 이용시간 데이터 저장 완료')
        return info



