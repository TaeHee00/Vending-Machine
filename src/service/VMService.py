import os
import sys
import copy
import json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import ManagerRepository
from repository import ManagerWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import UserRepository
from repository import DrinkRepository
from repository import VM_DrinkRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao
from src import Server


class VMService:

    def __init__(self):
        self.vmDrinkRepository = VM_DrinkRepository.VM_DrinkRepository()
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.cardRepository = CardRepository.CardRepository()
        self.userRepository = UserRepository.UserRepository()
        self.drinkRepository = DrinkRepository.DrinkRepository()
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

    def cashReturn(self, cash_dict):
        wallte_cash_data = self.managerWallteRepository.findCash()
        cash_seq_list = list()
        cash_data = dict()

        for cash in wallte_cash_data:
            cash_seq_list.append(cash[1])

        for cash in cash_seq_list:
            data = self.cashRepository.findCash(cash)[0]
            cash_data[data[1]] = data[0]

        cash_list = copy.deepcopy(cash_dict)
        del cash_list['total']
        for cash in cash_list:
            # 투입된 현금이 없으면 다음 현금으로 반환
            if cash_list[cash] <= 0:
                continue

            cash_seq = cash_data[cash]
            for _ in range(int(cash_list[cash])):
                self.cashRepository.decreaseCash(cash_seq)

    def drinkStockDecrease(self, drink_name):
        drink_seq = self.drinkRepository.findDrink(drink_name)[0]
        self.vmDrinkRepository.decreaseStock(drink_seq)
        return drink_seq

    def cashIncrease(self, drink_price):
        card_data = self.managerWallteRepository.findCard()
        card_seq = card_data[2]
        self.cardRepository.increaseCard(card_seq, drink_price)

    def vmCashStock(self):
        wallte_cash_list = self.managerWallteRepository.findCash()

        cash_seq = list()
        for cash in wallte_cash_list:
            cash_seq.append(cash[1])

        cash_stock = dict()
        for seq in cash_seq:
            cash_data = self.cashRepository.findCash(seq)[0]
            cash_stock[cash_data[1]] = cash_data[2]

        return cash_stock

# vm = VMService()
# vm.cashReturn(123)
