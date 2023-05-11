import pymysql
from Repository import Repository


# TODO dao에서 객체로 변경
class UserRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM user"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    # TODO 회원가입 기능
    def create(self):
        pass

    # TODO 유저 정보 수정
    def update(self):
        pass

    # TODO 유저 정보 삭제
    def delete(self):
        pass
