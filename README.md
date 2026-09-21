# 🌱 TripTune - OpenAPI 

TripTune-OpenAPI는 공공 데이터 포털의 한국관광공사 Tour API를 활용하여 여행지 및 지역 데이터를 수집·가공하고<br/>
TripTune 서비스에 필요한 데이터베이스를 구축하는 프로젝트입니다.

---
## 🛠 기술 스택
- **Language**: Python 3.12
- **API**: [공공 데이터 포털 - 한국관광공사 Tour API](https://www.data.go.kr/data/15101578/openapi.do) 
- **Database**: MySQL
- **Infra**: AWS EC2, AWS S3
- **Library** : 
  - Requests - 공공 데이터 API 호출
  - PyMySQL - MySQL 데이터 저장
  - Boto3 - AWS S3 이미지 저장
  - Pillow - 이미지 처리
  - python-dotenv - 환경 변수 관리
  - SSHTunnel / Paramiko - SSH 터널링
---
## ✨ 주요 기능
- 공공 데이터 포털 API를 활용한 지역, 시군구 데이터 수집
- 공공 데이터 포털 API를 활용한 여행지 데이터 수집
- 공공 데이터 포털 API를 활용한 여행지 이미지 데이터 수집
- 수집한 데이터를 가공하여 여행지 데이터를 MySQL에 저장
- 수집한 여행지 이미지를 S3에 저장

---

## 📂 파일 구조

```
TripTune-Open-API
├── src/
│   ├── api/                                
│   │   └── api_handler.py                  # 공공 데이터 포털 API 요청 및 파싱
│   ├── aws/
│   │   └── s3_handler.py                   # S3 설정 및 연동 
│   ├── data/
│   │   ├── data_cleaner.py                 # DB에 저장된 데이터 정제 및 가공
│   │   ├── data_collector_area.py          # 도시, 시군구 데이터 수집
│   │   ├── data_collector_image.py         # 여행지 이미지 데이터 수집
│   │   └── data_collector_travel.py        # 여행지 데이터 수집
│   ├── db/
│   │   ├── area_db.py                      # 도시, 시군구 관련 SQL 쿼리            
│   │   ├── content_type_db.py              # 여행지 타입 관련 SQL 쿼리
│   │   ├── db_handler.py                   # DB 연결 및 관리
│   │   ├── travel_image_db.py              # 여행지 이미지 관련 SQL 쿼리 
│   │   └── travel_place_db.py              # 여행지 관련 SQL 쿼리
│   ├── model/
│   │   ├── location.py                     # 도시, 시군구 모델              
│   │   ├── travel_image.py                 # 여행지 이미지 모델
│   │   └── travel_place.py                 # 여행지 모델
│   ├── utils/
│   │   ├── api_config.py                   # 공공 데이터 포털 API 요청 설정             
│   │   ├── log_handler.py                  # 로그 관리
│   │   └── utils.py                        # 날짜, 이미지 및 여행지 이용시간 데이터 정제
│   └── main.py                             # 프로젝트 실행
└── requirements.txt                        # 패키지 의존성 관리
```

---
## 🔐 환경 변수

실행에 필요한 환경 변수는 `.env` 파일에 설정합니다.

| 환경 변수 | 설명 |
|---|---|
| `SECRET_KEY` | 한국관광공사 Tour API 인증키 |
| `DB_HOST` | MySQL 서버 주소 |
| `DB_PORT` | MySQL 포트 |
| `DB_USERNAME` | MySQL 사용자명 |
| `DB_PASSWORD` | MySQL 비밀번호 |
| `DB_NAME` | MySQL 데이터베이스명 |
| `SSH_HOST` | SSH 서버 주소 |
| `SSH_PORT` | SSH 포트 |
| `SSH_USERNAME` | SSH 사용자명 |
| `SSH_PKEY` | SSH 접속 키 |
| `S3_REGION` | S3 리전 |
| `S3_BUCKET_NAME` | S3 버킷명 |
| `AWS_ACCESS_KEY_ID` | AWS 액세스 키 |
| `AWS_SECRET_ACCESS_KEY` | AWS 시크릿 키 |



---
## 🚀 실행 방법

### 1. 저장소 클론
```commandline
git clone <repository-url>
cd TripTune-OpenAPI
```
<br>

### 2. 가상환경 생성 및 활성화
```commandline
python -m venv venv
```
Windows:
```commandline
venv\Scripts\activate
```
macOS / Linux:
```commandline
source venv/bin/activate
```
<br>


### 3. 패키지 설치
```commandline
pip install -r requirements.txt
```
<br>

### 4. 환경 변수 설정
프로젝트 루트에 .env 파일을 생성하고 필요한 환경 변수를 설정합니다.

<br>

### 5. 프로젝트 실행
> `main.py`의 `save_travel_places()` 인자를 수정하여 수집 지역, 여행지 타입 및 수집 개수를 변경할 수 있습니다.
```commandline
python src/main.py
```
main.py에 설정된 지역과 여행지 타입을 기준으로 한국관광공사 Tour API에서 데이터를 수집하고 MySQL 및 S3에 저장합니다.

---
## 🔄 데이터 수집 과정
1. `save_travel_places()`에 지정한 지역, 여행지 타입, 수집 개수에 맞춰 데이터 수집을 실행합니다.
2. 데이터베이스에서 지역 및 콘텐츠 타입 정보를 조회해 API 요청 파라미터를 구성합니다.
3. 첫 요청 시 해당 조건의 전체 API 데이터 개수를 확인하고 수집 개수에 맞춰 필요한 요청 횟수를 계산합니다.
4. 요청마다 남은 데이터 개수를 계산해 불필요한 API 요청 횟수를 줄입니다.
5. 위도/경도 정보가 없는 여행지는 수집 대상에서 제외합니다.
6. 데이터베이스에서 해당 여행지의 기존 저장 여부를 확인합니다.
7. 저장된 여행지가 있고 수정 시간이 변경되지 않았다면 수집하지 않습니다.
8. 변경된 여행지이거나 신규 여행지인 경우 상세 정보와 썸네일 이미지를 조회하고 저장합니다.
   - 여행지 설명 데이터가 없는 여행지는 수집 대상에서 제외합니다. 
   - 변경된 여행지인 경우 기존 데이터를 갱신합니다. 
   - 신규 여행지인 경우 데이터를 신규 저장합니다.
9. 신규 또는 변경된 여행지의 상세 이미지를 저장합니다.
   - 기존 상세 이미지가 있는 경우 신규 이미지를 저장한 후 기존 이미지를 삭제합니다.
10. API 요청 등 수집 과정에서 오류가 발생하면 데이터베이스 변경 사항을 롤백합니다.
