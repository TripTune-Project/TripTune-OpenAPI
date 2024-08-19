import urllib
import requests


def get_json_data(url, params):
    # parameter 인코딩 후 데이터 요청
    encoding_params = urllib.parse.urlencode(params, safe='#\':()+=%,')

    response = requests.get(url, params=encoding_params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"요청 실패: 상태코드 {response.status_code}")
        return 



def get_total_count(url, params):
    content = get_json_data(url, params)
    print(content)
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