import sys
import urllib
import requests
import xml.etree.ElementTree as ET


def get_json_data(url, params):
    # parameter 인코딩 후 데이터 요청
    encoding_params = urllib.parse.urlencode(params, safe='#\':()+=%,')

    response = requests.get(url, params=encoding_params)
    content_type = response.headers.get("Content-Type")

    if response.status_code == 200:
        if "application/json" in content_type:
            try:
                return response.json()
            except ValueError as e:
                print(f"JSON 파싱 오류: {e}")
                sys.exit(1)
        elif "application/xml" in content_type or "text/xml" in content_type:
            try:
                root = ET.fromstring(response.text)
                print(f"에러 코드 : {root.find('.//returnReasonCode').text}\n에러 메시지 : {root.find('.//returnAuthMsg').text}")
                sys.exit(1)
            except ET.ParseError as e:
                print("XML 파싱 오류 : {e}")
                sys.exit(1)
        else:
            print(f"알 수 없는 컨텐츠 타입 : {content_type}")
            sys.exit(1)
    else:
        print(f"요청 실패: 상태코드 {response.status_code}\n컨텐츠 타입 : {content_type}")
        sys.exit(1)



def get_total_count(url, params):
    content = get_json_data(url, params)
    return content["response"]["body"]["totalCount"]




def fetch_items(url, params, total_count):
    items = []
    iterations = (total_count - 1) // params["numOfRows"] + 2

    for pageNo in range(1, iterations):
        params["pageNo"] = pageNo

        content = get_json_data(url, params)
        print(content)
        
        items.extend(content["response"]["body"]["items"]["item"])
        
    return items