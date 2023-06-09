# from Repository import Repository
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository


class VM_DrinkRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM vm_drink"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    def decreaseStock(self, drink_seq):
        self.query = "UPDATE vm_drink SET vm_drink.amount = vm_drink.amount - 1 WHERE vm_drink.drink_seq = (%s)"
        data = (drink_seq)
        self.cursor.execute(self.query, data)
        self.db.commit()

    def increaseStock(self, drink_seq, drink_num):
        self.query = "UPDATE vm_drink SET vm_drink.amount = CONCAT(vm_drink.amount + (%s)) WHERE vm_drink.drink_seq = (%s)"
        data = (drink_num, drink_seq)
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
#
# vd = VM_DrinkRepository()
# vd.increaseStock(1, 1)
