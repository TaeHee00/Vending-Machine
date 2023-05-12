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

    def userCashList(self, user_seq):
        cash_list = self.userService.userCashList(user_seq)
        return cash_list

    def userCardList(self, user_seq):
        card_list = self.userService.userCardList(user_seq)
        return card_list

    def userRegister(self, userDao):
        res = self.userService.userRegister(userDao)
        return res

    def userList(self):
        res = self.userService.userList()
        return res


# # for drink in dc.drinkList():
# #     print(drink, d)
# uc = UserController()
# print(uc.userCardList(1))