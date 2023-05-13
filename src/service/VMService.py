import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import ManagerRepository
from repository import ManagerWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import UserRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao


class VMService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.cardRepository = CardRepository.CardRepository()
        self.userRepository = UserRepository.UserRepository()
        self.managerRepository = ManagerRepository.ManagerRepository()
        self.managerWallteRepository = ManagerWallteRepository.ManagerWallteRepository()

    def managerCashInjection(self, cash_name):
        # TODO managerWallteRepository에서 cash sequence 받아오기
        cash_list = self.managerWallteRepository.findCash()
        # TODO cashRepository에 cash sequence로 increase
        for cash in cash_list:
            cash_data = self.cashRepository.findCash(cash[1])[0]
            # cash sequence에 담긴 정보가 유저가 선택한 정보와 일치할 경우
            if cash_data[1] == cash_name:
                self.cashRepository.increaseCash(cash_data[0])
                break

# vm = VMService()
# vm.managerCashInjection('1000')
