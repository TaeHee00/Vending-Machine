import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from service import UserService
from dao import VM_DrinkDao
from dao import DrinkDao


class UserController:

    def __init__(self):
        self.userService = UserService.UserService()

    def cardList(self):
        card_list = self.userService.cardList()
        return card_list

    def cashList(self):
        cash_list = self.userService.cashList()
        return cash_list


# for drink in dc.drinkList():
#     print(drink, d)
# uc = UserController()
# print(uc.cardList()[0].getCardName())