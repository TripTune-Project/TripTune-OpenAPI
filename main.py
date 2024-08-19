import os
from dotenv import load_dotenv
from db_handler import DatabaseHandler
from data_collector import *


def main():
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL")
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_port = int(os.getenv("DB_PORT"))

    if not all([secret_key, base_url, db_host, db_user, db_password, db_name, db_port]):
        print("환경 변수 불러오기 실패")
        return


    db = DatabaseHandler(db_host, db_user, db_password, db_name, db_port)
    
    try:
        # korea_city_code(db, secret_key, base_url)
        # korea_district_code(db, secret_key, base_url)
        # korea_category1_code(db, secret_key, base_url)
        # korea_category2_code(db, secret_key, base_url)
        # korea_category3_code(db, secret_key, base_url)
        korea_area_based_list(db, secret_key, base_url)
        
    finally:
        db.close()



if __name__ == '__main__':
    main()
