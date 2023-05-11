import pymysql


class UserRepository:

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
        # query = "INSERT INTO LOGIN_DATA (USER_CODE, ID, PW) VALUES (%s, %s, %s)"
        # data = ('3', 'member_id', 'member_pw')
        #
        # cursor.execute(query, data)
        # db.commit()

    def find(self, table):
        self.query = f"SELECT * FROM {table}"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


ur = UserRepository()

print(ur.find('user'))
