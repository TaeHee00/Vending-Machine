import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from service import UserService
from service import ManagerService
from dao import VM_DrinkDao
from dao import DrinkDao


class ManagerController:

    def __init__(self):
        self.managerService = ManagerService.ManagerService()


    def findManagerBank(self):
        managerBank = self.managerService.findManagerBank()
        return managerBank

    def decreaseManagerBank(self, money):
        self.managerService.decreaseManagerBank(money)
        pass

    def increaseDrink(self, drink_seq, drink_num):
        self.managerService.increaseDrink(drink_seq, drink_num)
        pass

    def findCash(self):
        manager_cash_data = self.managerService.findManagerCash()
        return manager_cash_data
        pass

    def increaseCash1000(self):
        self.managerService.increaseCash1000()

    def increaseCash500(self):
        self.managerService.increaseCash500()

    def increaseCash100(self):
        self.managerService.increaseCash100()