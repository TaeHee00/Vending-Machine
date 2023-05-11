import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import CardRepository
from repository import CashRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao


class UserService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.cardRepository = CardRepository.CardRepository()

    def cardList(self):
        card_list = list()

        for card in self.cardRepository.find():
            # card[0], card[1], card[2]
            # 순서대로 고유번호, 카드명, 카드잔액
            card_dao = CardDao.CardDao(card[0], card[1], card[2])
            card_list.append(card_dao)

        return card_list

    def cashList(self):
        cash_list = list()

        for cash in self.cashRepository.find():
            # card[0], card[1], card[2]
            # 순서대로 고유번호, 카드명, 카드잔액
            cash_dao = CashDao.CashDao(cash[0], cash[1], cash[2])
            cash_list.append(cash_dao)

        return cash_list
