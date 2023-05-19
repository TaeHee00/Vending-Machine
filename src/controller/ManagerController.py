import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from service import UserService
from dao import VM_DrinkDao
from dao import DrinkDao


class ManagerController:

    def __init__(self):
        self.managerService = ManagerService.ManagerService()

