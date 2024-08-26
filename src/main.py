import os
from dotenv import load_dotenv
from db.db_handler import DatabaseHandler
from data.data_collector_area import *
from data.data_collector_category import *
from data.data_collector_travel import *
from aws.s3_handler import *


def main():
    load_dotenv()

    # tour api
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")

    # database
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = int(os.getenv("DB_PORT"))

    # s3
    s3_region_name = os.getenv("S3_REGION")
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    aws_accees_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    if not all([secret_key, base_url, db_host, db_user, db_password, db_name, db_port, s3_region_name, s3_bucket_name, aws_accees_key_id, aws_secret_access_key]):
        print("환경 변수 불러오기 실패")
        return None


    db = DatabaseHandler(db_host, db_user, db_password, db_name, db_port)
    s3 = S3Handler(s3_region_name, s3_bucket_name, aws_accees_key_id, aws_secret_access_key)
    
    try:
        # korea_city_code(db, secret_key, base_url)
        # korea_district_code(db, secret_key, base_url)
        # korea_category1_code(db, secret_key, base_url)
        # korea_category2_code(db, secret_key, base_url)
        # korea_category3_code(db, secret_key, base_url)
        # korea_area_based_list(db, s3, secret_key, base_url)
        # korea_detail_common(db, secret_key, base_url)
        # korea_specific_area_based_list(db, s3, secret_key, base_url, '서울', '강남구')
        korea_limited_area_based_list(db, s3, secret_key, base_url, '제주도', '서귀포시')
    finally:
        db.close()



if __name__ == '__main__':
    main()
