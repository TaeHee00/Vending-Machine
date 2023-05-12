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

    def userList(self):
        res = self.userRepository.find()
        return res

    def userCashList(self, user_seq):
        user_wallte_cash_data = self.userWallteRepository.findUserCash(user_seq)

        user_cash_list = list()
        for wallte_cash in user_wallte_cash_data:
            cash_data = self.cashRepository.findUserCash(wallte_cash[1])[0]
            # TODO dao -> dto
            cash_dao = CashDao.CashDao(cash_data[0], cash_data[1], cash_data[2])
            user_cash_list.append(cash_dao)

        return user_cash_list

    def userCardList(self, user_seq):
        user_wallte_card_data = self.userWallteRepository.findUserCard(user_seq)

        user_card_list = list()
        for wallte_card in user_wallte_card_data:
            card_data = self.cardRepository.findUserCard(wallte_card[2])[0]
            # TODO dao -> dto
            card_dao = CardDao.CardDao(card_data[0], card_data[1], card_data[2])
            user_card_list.append(card_dao)

        return user_card_list

# us = UserService()
# print(us.userCardList(1))