# from Repository import Repository
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository
# from repository.CardRepository import CardRepository
# from repository.CashRepositroy import CashRepository


class ManagerWallteRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM manager_wallte"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def findCash(self):
        self.query = "SELECT * FROM manager_wallte WHERE manager_wallte.flag = 'cash'"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    # def findUserCard(self, user_seq):
    #     self.query = "SELECT * FROM user_wallte WHERE user_wallte.user_seq = (%s) AND user_wallte.flag = 'card'"
    #     data = (user_seq)
    #     self.cursor.execute(self.query, data)
    #     self.result = self.cursor.fetchall()
    #     return self.result

    # TODO 회원가입 기능
    def create(self):
        pass

    # TODO 유저 정보 수정
    def update(self):
        pass

    # TODO 유저 정보 삭제
    def delete(self):
        pass

#
# uwr = UserWallteRepository()
# print(uwr.findUserCash("1"))