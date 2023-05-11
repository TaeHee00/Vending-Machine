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

    # TODO 회원가입 기능
    def create(self):
        pass

    # TODO 유저 정보 수정
    def update(self):
        pass

    # TODO 유저 정보 삭제
    def delete(self):
        pass
