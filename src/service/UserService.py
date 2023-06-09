import os
import sys
import copy

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import UserRepository
from repository import UserBagRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao


class UserService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.userBagRepository = UserBagRepository.UserBagRepository()
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
            cash_data = self.cashRepository.findCash(wallte_cash[1])[0]
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

    def userCashDecrease(self, user_seq, select_cash):
        user_wallte_cash_data = self.userWallteRepository.findUserCash(user_seq)

        user_cash_list = list()
        for wallte_cash in user_wallte_cash_data:
            # 사용자 지갑의 들어있는 현금 고유 번호를 통해 현금의 정보를 가져온다.
            cash_data = self.cashRepository.findCash(wallte_cash[1])[0]
            # 현금의 이름이 선택한 현금과 같을때
            if cash_data[1] == select_cash:
                self.cashRepository.decreaseCash(wallte_cash[1])
                # print(wallte_cash[1])
                break

    def cashReturn(self, user_seq, cash_dict):
        wallte_cash_data = self.userWallteRepository.findUserCash(user_seq)

        cash_seq_list = list()
        cash_seq_data = dict()

        for cash in wallte_cash_data:
            cash_seq_list.append(cash[1])

        for cash in cash_seq_list:
            data = self.cashRepository.findCash(cash)[0]
            cash_seq_data[data[1]] = data[0]

        cash_list = copy.deepcopy(cash_dict)
        del cash_list['total']
        for cash in cash_list:
            # 반환된 현금이 없으면 다음 현금으로
            if cash_list[cash] <= 0:
                continue

            cash_seq = cash_seq_data[cash]
            for _ in range(int(cash_list[cash])):
                self.cashRepository.increaseCash(cash_seq)

    def cardDecrease(self, drink_price, card_seq):
        # print("UserService.cardDecrease", drink_price, card_seq)
        self.cardRepository.decreaseCard(card_seq, drink_price)

    def bagDrinkIncrease(self, user_seq, drink_seq):
        # 유저의 가방에 들어있는 음료 리스트를 가져온다.
        user_bag = self.userBagRepository.findUserDrink(user_seq)
        # 가져온 리스트에 구매한 음료가 있을 경우 증가,
        # 없을 경우 새롭게 데이터 생성
        isDrink = False
        for drink in user_bag:
            # 같은 음료가 있음
            if drink[1] == drink_seq:
                isDrink = True
                break

        if isDrink:
            self.userBagRepository.increaseStock(user_seq, drink_seq)
        else:
            self.userBagRepository.createStock(user_seq, drink_seq)
#
# us = UserService()
# print(us.bagDrinkIncrease(1, 1))
