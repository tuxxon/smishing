

import pymysql
import os

class Database():
    def __init__(self):
        self.db= pymysql.connect(
            host=os.getenv('FLASK_DB'),
            user='root',
            password='password',
            db='smishing',
            charset='utf8'
            )
        self.cursor= self.db.cursor(pymysql.cursors.DictCursor)
 
    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args) 
 
    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchone()
        return row
 
    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row
 
    def commit(self):
        self.db.commit()
