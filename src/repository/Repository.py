import pymysql


class Repository:

    def __init__(self):
        self.db = pymysql.Connect(
            host='localhost',
            user='root',
            password='Skdlxmfhem3323!',
            database='vending_machine',
            charset="utf8"
        )
        self.cursor = self.db.cursor()
        self.query = ""
        self.result = None

    def find(self):
        # self.query = f"SELECT * FROM {table}"
        # self.cursor.execute(self.query)
        # self.result = self.cursor.fetchall()
        # return self.result
        pass