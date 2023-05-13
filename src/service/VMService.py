import os
import sys
import copy

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository import UserRepository
from repository import UserWallteRepository
from repository import ManagerRepository
from repository import ManagerWallteRepository
from repository import CardRepository
from repository import CashRepository
from repository import UserRepository
# from repository import UserBagRepository
from dao import CardDao
from dao import CashDao


class VMService:

    def __init__(self):
        self.userWallteRepository = UserWallteRepository.UserWallteRepository()
        self.cashRepository = CashRepository.CashRepository()
        self.cardRepository = CardRepository.CardRepository()
        self.userRepository = UserRepository.UserRepository()
        self.managerRepository = ManagerRepository.ManagerRepository()
        self.managerWallteRepository = ManagerWallteRepository.ManagerWallteRepository()

    def managerCashInjection(self, cash_name):
        # TODO managerWallteRepository에서 cash sequence 받아오기
        cash_list = self.managerWallteRepository.findCash()
        # TODO cashRepository에 cash sequence로 increase
        for cash in cash_list:
            cash_data = self.cashRepository.findCash(cash[1])[0]
            # cash sequence에 담긴 정보가 유저가 선택한 정보와 일치할 경우
            if cash_data[1] == cash_name:
                self.cashRepository.increaseCash(cash_data[0])
                break

    def cashReturn(self, cash_dict):
        wallte_cash_data = self.managerWallteRepository.findCash()
        cash_seq_list = list()
        cash_data = dict()

        for cash in wallte_cash_data:
            cash_seq_list.append(cash[1])

        for cash in cash_seq_list:
            data = self.cashRepository.findCash(cash)[0]
            cash_data[data[1]] = data[0]

        cash_list = copy.deepcopy(cash_dict)
        del cash_list['total']
        for cash in cash_list:
            # 투입된 현금이 없으면 다음 현금으로 반환
            if cash_list[cash] <= 0:
                continue

            cash_seq = cash_data[cash]
            for _ in range(int(cash_list[cash])):
                self.cashRepository.decreaseCash(cash_seq)

    def drink_buy(self, drink_name):
        # TODO cash인지 card인지 확인

        # TODO Card일 경우
        # TODO Card 잔액 감소
        # TODO Interface의 Card 잔액 수정
        # TODO VM drink 재고 감소
        # TODO User Bag에 추가
        # TODO Manager_Bank에 잔액 추가

        # TODO Cash일 경우
        # TODO UserApplication -> self.temp_cash_cnt['total']을 음료수 가격 만큼 감소
        # TODO UserApplication -> self.temp_cash_cnt 화폐 개수 수정
        # TODO 화폐개수수정) 전부 개수 0으로 변경 후 그리디 알고리즘을 사용하여 가장 반환에 가장 적합한 화폐 선정
        # TODO VM_Machine에 화폐가 부족할 경우 down-casting 하여 반환
        # TODO VM_Machine에 화폐가 부족할 경우 알람 or Print문으로 경고
        # TODO Interface의 Cash 투입 금액 수정
        # TODO VM drink 재고 감소
        # TODO User Bag에 추가
        pass

        # user_wallte_cash_data = self.userWallteRepository.findUserCash(user_seq)
        #
        # user_cash_list = list()
        # for wallte_cash in user_wallte_cash_data:
        #     # 사용자 지갑의 들어있는 현금 고유 번호를 통해 현금의 정보를 가져온다.
        #     cash_data = self.cashRepository.findCash(wallte_cash[1])[0]
        #     # 현금의 이름이 선택한 현금과 같을때
        #     if cash_data[1] == select_cash:
        #         self.cashRepository.decreaseUserCash(wallte_cash[1])
        #         # print(wallte_cash[1])
        #         break
#
# vm = VMService()
# vm.cashReturn(123)
