import pymysql

class DatabaseHandler:
    def __init__(self, host, user, password, db, port):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port,
            charset="utf8"
        )
        self.cursor = self.conn.cursor()

    def execute_select_all(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute_select_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def execute_insert(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()
    
    def close(self):
        self.conn.close()