import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from service import DrinkService
from dao import VM_DrinkDao
from dao import DrinkDao


class DrinkController:

    def __init__(self):
        self.drinkService = DrinkService.DrinkService()

    def drinkList(self):
        drink_list = self.drinkService.drinkList()
        return drink_list

    def vmDrinkList(self):
        drink_list = self.drinkService.vmDrinkList()
        return drink_list


# for drink in dc.drinkList():
#     print(drink, d)
# print(dc.drinkService)