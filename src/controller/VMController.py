import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from service import VMService
from dao import VM_DrinkDao
from dao import DrinkDao


class VMController:

    def __init__(self):
        self.vmService = VMService.VMService()

    def managerCashInjection(self, cash_name):
        self.vmService.managerCashInjection(cash_name)

    def cashReturn(self, cash_dict):
        self.vmService.cashReturn(cash_dict)

    def drink_buy(self, drink_name, drink_price, user_seq):
        self.vmService.drink_buy(drink_name, drink_price)

    def drinkStockDecrease(self, drink_name):
        drink_seq = self.vmService.drinkStockDecrease(drink_name)
        return drink_seq

    def cashIncrease(self, drink_price):
        self.vmService.cashIncrease(drink_price)

    def vmCashStock(self):
        cash_stock = self.vmService.vmCashStock()
        return cash_stock
# # for drink in dc.drinkList():
# #     print(drink, d)
# uc = UserController()
# print(uc.userCardList(1))