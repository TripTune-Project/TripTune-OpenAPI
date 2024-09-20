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

    def execute_select_area_one(self, country, city, district):
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

    def execute_select_area_all(self):
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

    def execute_update(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute_last_inserted_id(self):
        return self.cursor.lastrowid
    
    def close(self):
        self.conn.close()
    
    