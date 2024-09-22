import pymysql

class DatabaseHandler:
    def __init__(self, host, user, password, db, port):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def execute_select_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_select_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def select_area_one(self, country, city, district):
        select_city_and_district = '''SELECT
                                        ct.country_id, ct.country_name,
                                        c.city_id, c.city_name, c.api_area_code,
                                        d.district_id, d.district_name, d.api_sigungu_code
                                    FROM district d
                                    INNER JOIN city c
                                    ON d.city_id = c.city_id
                                    INNER JOIN country ct
                                    ON c.country_id = ct.country_id
                                    WHERE ct.country_name = %s
                                    AND c.city_name = %s
                                    AND d.district_name = %s
                                    '''
                                
        self.cursor.execute(select_city_and_district, (country, city, district))
        return self.cursor.fetchone()

    def select_area_all(self):
        select_city_and_district = '''SELECT
                                    ct.country_id, ct.country_name,
                                    c.city_id, c.city_name, c.api_area_code,
                                    d.district_id, d.district_name, d.api_sigungu_code
                                FROM district d
                                INNER JOIN city c
                                ON d.city_id = c.city_id
                                INNER JOIN country ct
                                ON c.country_id = ct.country_id
                                '''
        self.cursor.execute(select_city_and_district)
        return self.cursor.fetchall()

    def execute_insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()


    def insert_travel_place(self, travel_place):
        insert_travel_place = '''INSERT INTO travel_place(country_id, city_id, district_id, category_code, content_type_id, place_name, address, detail_address
                                            , longitude, latitude, api_content_id, created_at, api_created_at, api_updated_at) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s)'''

        self.cursor.execute(insert_travel_place, (
            travel_place.location.country_id, 
            travel_place.location.city_id, 
            travel_place.location.district_id, 
            travel_place.category_code, 
            travel_place.content_type_id, 
            travel_place.place_name, 
            travel_place.address, 
            travel_place.detail_address, 
            travel_place.longitude, 
            travel_place.latitude, 
            travel_place.api_content_id, 
            travel_place.api_created_at, 
            travel_place.api_updated_at
        ))
        
        self.conn.commit()

    def insert_category(self, category):
        insert_category = 'INSERT INTO api_category(category_code, category_name, parent_code, level) VALUES (%s, %s, %s, %s)'

        self.cursor.execute(insert_category, (
            category.category_code,
            category.category_name,
            category.parent_code,
            category.level
        ))

        self.conn.commit()
                

    def execute_update(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute_last_inserted_id(self):
        return self.cursor.lastrowid
    
    def close(self):
        self.conn.close()
    
    