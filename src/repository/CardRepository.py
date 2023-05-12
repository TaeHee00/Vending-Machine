import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository


class CardRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM card"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def findCreateCard(self):
        card_list = self.find()
        return card_list[-1]

    def findUserCard(self, card_seq):
        self.query = "SELECT * FROM card WHERE card.card_seq = (%s)"
        data = (card_seq)
        self.cursor.execute(self.query, data)
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