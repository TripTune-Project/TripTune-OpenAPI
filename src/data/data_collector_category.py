from api.api_handler import *
from utils.utils import *
from utils.log_handler import setup_logger
from model.category import Category
from db.db_handler import DatabaseHandler


logger = setup_logger()

def korea_category1_code(db, secret_key, base_url):
    '''
    관광지 카테고리 중 대분류(cat1)를 조회 및 저장한다.


    [Parameter]
    db: mysql 데이터베이스 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    '''
    url = base_url + '/categoryCode1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    total_count = get_total_count(url, params)
    items = fetch_items(url, params, total_count)

    for item in items:
        category = Category(
            category_code=item['code'],
            category_name=item['name'],
            parent_code=None,
            level=1
        )

        db.insert_category(category)

    logger.info('korea_category1_code() - 카테고리(cat1) 데이터 저장 완료')


# 중분류 카테고리(cat2) 조회 및 저장
def korea_category2_code(db, secret_key, base_url):
    '''
    관광지 카테고리 중 중분류(cat2)를 조회 및 저장한다.
    api 요청 시 parameter 중 cat1 에 open api 에서 지정한 대분류 카테고리(cat1) id 값을 넣어 요청한다.
    부모 컬럼(parent_code)에 대분류(cat1)의 id를 DB에서 조회해 같이 저장한다.


    [Parameter]
    db: mysql 데이터베이스 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    '''
    url = base_url + '/categoryCode1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    # 부모(대분류) 카테고리 조회
    categoris = db.execute_select_all('SELECT * FROM api_category WHERE LEVEL = 1')

    for category in categoris:
        cat1_code = category['category_code']
        params['cat1'] = cat1_code

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)
        
        for item in items:
            category = Category(
                category_code=item['code'],
                category_name=item['name'],
                parent_code=cat1_code,
                level=2
            )

            db.insert_category(category)

    logger.info('korea_category2_code() - 카테고리(cat2) 데이터 저장 완료')



def korea_category3_code(db, secret_key, base_url):
    '''
    관광지 카테고리 중 소분류(cat3)를 조회 및 저장한다.
    api 요청 시 parameter 중 cat1, cat2 에 open api 에서 지정한 대분류 카테고리(cat1), 중분류 카테고리(cat2) id 값을 넣어 요청한다.
    부모 컬럼(parent_code)에 중분류(cat2)의 id를 DB에서 조회해 같이 저장한다.


    [Parameter]
    db: mysql 데이터베이스 연결
    secret_key: open api 연동을 위해 사용할 키
    base_url: open api url 정보
    '''
    url = base_url + '/categoryCode1'

    params = {
        'serviceKey': secret_key,
        'numOfRows': 10,
        'pageNo': 1,
        'MobileOS': 'ETC',
        'MobileApp': 'TripTune',
        '_type': 'json'
    }

    # 부모(중분류) 카테고리 조회
    categoris = db.execute_select_all('SELECT * FROM api_category WHERE LEVEL = 2')


    for category in categoris:
        cat2_code = category['category_code']
        params['cat1'] = category['parent_code']
        params['cat2'] = cat2_code

        total_count = get_total_count(url, params)
        items = fetch_items(url, params, total_count)

        for item in items:
            category = Category(
                category_code=item['code'],
                category_name=item['name'],
                parent_code=cat2_code,
                level=3
            )

            db.insert_category(category)

    logger.info('korea_category3_code - 카테고리(cat3) 데이터 저장 완료')
