import sys
import urllib
import requests
import xml.etree.ElementTree as ET
from utils.log_handler import setup_logger


logger = setup_logger()

def get_json_data(url, params):
    '''
    api 요청 후 json으로 변환한다.
    요청 시 특수문자로 인한 오류를 방지하기 위해 파라미터 값들을 인코딩한다.
    
    * open api 요청 결과가 XML 인 경우 에러 페이지이기 때문에 그에 따른 try-except를 추가하였다.


    [Parameter]
    url: open api 요청 url
    params: open api 요청 파라미터
    '''
    encoding_params = urllib.parse.urlencode(params, safe='#\':()+=%,')

    response = requests.get(url, params=encoding_params)
    content_type = response.headers.get('Content-Type')

    if response.status_code == 200:
        if 'application/json' in content_type:
            try:
                return response.json()
            except ValueError as e:
                logger.error(f'JSON 파싱 오류: {e}')
                sys.exit(1)
        elif 'application/xml' in content_type or 'text/xml' in content_type:
            try:
                root = ET.fromstring(response.text)
                logger.error(f'에러 코드 : {root.find(".//returnReasonCode").text}\n에러 메시지 : {root.find(".//returnAuthMsg").text}')
                sys.exit(1)
            except ET.ParseError as e:
                logger.error('XML 파싱 오류 : {e}')
                sys.exit(1)
        else:
            logger.error(f'알 수 없는 컨텐츠 타입 : {content_type}')
            sys.exit(1)
    else:
        logger.error(f'요청 실패: 상태코드 {response.status_code}\n컨텐츠 타입 : {content_type}')
        sys.exit(1)



def get_total_count(url, params):
    '''
    get_json_data 함수를 통해 api 요청 후 요청 결과의 총 데이터 갯수를 찾아 반환한다.


    [Parameter]
    url: open api 요청 url
    params: open api 요청 파라미터

    [Return]
    (int) content : 요청 결과인 아이템 총 갯수
    '''
    content = get_json_data(url, params)
    return content['response']['body']['totalCount']




def fetch_items(url, params, total_count):
    '''
    get_json_data 함수를 통해 api 요청해 요청 결과에 item 만 추출해서 리스트에 저장한다.
    total_count 로 총 페이지 수(pageNo) 를 계산해 반복문에 이용한다.

    *api 요청 결과는 {'response':{'header':{...}, 'body':{'items':'item':[]}}} 으로 구성되어 있다.

    [Parameter]
    url: open api 요청 url
    params: open api 요청 파라미터
    total_count: 요청 결과인 아이템 총 갯수

    [Return]
    items : 요청 결과 중 item 값만 담은 리스트
    '''
    items = []
    iterations = (total_count - 1) // params['numOfRows'] + 2

    for pageNo in range(1, iterations):
        params['pageNo'] = pageNo

        content = get_json_data(url, params)
        print(content)
        
        items.extend(content['response']['body']['items']['item'])
        
    return items