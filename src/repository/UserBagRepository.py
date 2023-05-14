# from Repository import Repository
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository


class UserBagRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM user_bag"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    # def decreaseStock(self, drink_seq):
    #     self.query = "UPDATE vm_drink SET vm_drink.amount = vm_drink.amount - 1 WHERE vm_drink.drink_seq = (%s)"
    #     data = (drink_seq)
    #     self.cursor.execute(self.query, data)
    #     self.db.commit()

    def increaseStock(self, user_seq, drink_seq):
        self.query = "UPDATE user_bag SET user_bag.amount = user_bag.amount + 1 WHERE user_bag.user_seq = (%s) AND user_bag.drink_seq = (%s)"
        data = (user_seq, drink_seq)
        self.cursor.execute(self.query, data)
        self.db.commit()

    def createStock(self, user_seq, drink_seq):
        self.query = "INSERT INTO user_bag(user_seq, drink_seq, amount) VALUES (%s, %s, %s)"
        data = (user_seq, drink_seq, str(1))
        self.cursor.execute(self.query, data)
        self.db.commit()

    def findUserDrink(self, user_seq):
        self.query = "SELECT * FROM user_bag WHERE user_bag.user_seq = (%s)"
        data = (user_seq)
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
