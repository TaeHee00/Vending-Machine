import os
import sys
import copy

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from repository import UserRepository
from repository import UserWallteRepository
from repository import ManagerWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import VM_DrinkRepository
# from repository import UserRepository
# from repository import UserBagRepository


class ManagerService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.managerWallteRepository = ManagerWallteRepository.ManagerWallteRepository()
        self.cardRepository = CardRepository.CardRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.vmDrinkRepository = VM_DrinkRepository.VM_DrinkRepository()

    def findManagerBank(self):
        wallte_data = self.managerWallteRepository.findCard()
        card_seq = wallte_data[2]
        card_data = self.cardRepository.findUserCard(card_seq)[0][2]
        return card_data

    def decreaseManagerBank(self, money):
        wallte_data = self.managerWallteRepository.findCard()
        card_seq = wallte_data[2]
        self.cardRepository.decreaseCard(card_seq, money)

    def increaseDrink(self, drink_seq, drink_num):
        self.vmDrinkRepository.increaseStock(drink_seq, drink_num)

    def findManagerCash(self):
        cash_data = self.managerWallteRepository.findCash()
        seq_list = list()
        seq_list.append(cash_data[1][1])
        seq_list.append(cash_data[2][1])
        seq_list.append(cash_data[3][1])

        _cash_data = list()
        for seq in seq_list:
            _cash_data.append(self.cashRepository.findCash(seq)[0])
        return _cash_data

    def increaseCash1000(self):
        cash_data = self.managerWallteRepository.findCash()
        seq = cash_data[1][1]
        self.cashRepository.increaseCash(seq)
        pass

    def increaseCash500(self):
        cash_data = self.managerWallteRepository.findCash()
        seq = cash_data[2][1]
        self.cashRepository.increaseCash(seq)
        pass

    def increaseCash100(self):
        cash_data = self.managerWallteRepository.findCash()
        seq = cash_data[3][1]
        self.cashRepository.increaseCash(seq)
        pass

# ms = ManagerService()
# print(ms.findCash())
