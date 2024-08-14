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