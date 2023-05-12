import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import UserRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao


class UserService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.cardRepository = CardRepository.CardRepository()
        self.userRepository = UserRepository.UserRepository()

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

    def userRegister(self, userDao):
        # TODO 중복일 경우 회원가입 X
        # TODO 중복이 아닐 경우 회원가입
        res = self.userRepository.find()
        isFind = False
        for user in res:
            if user[1] == userDao.getUserId():
                isFind = True

        if isFind:
            return "중복"
        else:
            self.userRepository.save(userDao)
            return "성공"

