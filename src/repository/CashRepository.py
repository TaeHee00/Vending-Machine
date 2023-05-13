import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository


class CashRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM cash"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def findCash(self, cash_seq):
        self.query = "SELECT * FROM cash WHERE cash.cash_seq = (%s)"
        data = (cash_seq)
        self.cursor.execute(self.query, data)
        self.result = self.cursor.fetchall()
        return self.result

    def findCreateCash(self):
        cash_list = self.find()
        return (cash_list[-4], cash_list[-3], cash_list[-2], cash_list[-1])

    def decreaseCash(self, cash_seq):
        self.query = "UPDATE cash SET cash.amount = cash.amount - 1 WHERE cash.cash_seq = (%s)"
        data = (str(cash_seq))
        self.cursor.execute(self.query, data)
        self.db.commit()

    def increaseCash(self, cash_seq):
        self.query = "UPDATE cash SET cash.amount = cash.amount + 1 WHERE cash.cash_seq = (%s)"
        data = (str(cash_seq))
        self.cursor.execute(self.query, data)
        self.db.commit()

    # TODO 회원가입 기능
    def create(self):
        pass

    # TODO 유저 정보 수정
    def update(self):
        pass

    # TODO 유저 정보 삭제
    def delete(self):
        pass
