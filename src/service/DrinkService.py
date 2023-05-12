import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import DrinkRepository
from repository import VM_DrinkRepository
from dao import DrinkDao
from dao import VM_DrinkDao


class DrinkService:

    def __init__(self):
        self.drinkRepository = DrinkRepository.DrinkRepository()
        self.vmDrinkRepository = VM_DrinkRepository.VM_DrinkRepository()

    def drinkList(self):
        drink_list = list()

        for drink in self.drinkRepository.find():
            # drink[0], drink[1], drink[2]
            # 순서대로 고유번호, 음료명, 음료가격(원가)
            drink_dao = DrinkDao.DrinkDao(drink[0], drink[1], drink[2])
            drink_list.append(drink_dao)

        return drink_list

    def vmDrinkList(self):
        drink_list = list()

        for drink in self.vmDrinkRepository.find():
            drink_dao = VM_DrinkDao.VM_DrinkDao(drink[0], drink[1], drink[2], drink[3])
            drink_list.append(drink_dao)

        return drink_list
