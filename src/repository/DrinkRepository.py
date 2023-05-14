# from Repository import Repository
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository


class DrinkRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM drink"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def findDrink(self, drink_name):
        self.query = "SELECT * FROM drink WHERE drink.drink_name = (%s)"
        data = (drink_name)
        self.cursor.execute(self.query, data)
        self.result = self.cursor.fetchone()
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
