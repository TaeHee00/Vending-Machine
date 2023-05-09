import json
import Card
import Cash
from Manager import PayManager


class User:

    def __init__(self):
        self.wallet = {
            "Cash": Cash.Cash(),
            "Card": Card.Card()
        }

        with open("user_bag.json", "r") as file:
            self.bag = json.load(file)['bag']

    # TODO 현금 투입 기능
    def cash_injection(self, choice):
        card_name = choice.replace(":", "").replace("원", "").split()[0]
        print(card_name)

    # TODO 현금 반환  기능
    def cash_return(self):
        pass

    # TODO 카드 투입 기능
    def card_injection(self, choice):
        card_name = choice.replace(":", "").split()[0]
        # 선택한 카드의 잔액
        card_balance = self.wallet['Card'].get_balance(card_name)
        # 결제시스템에 카드 정보 등록
        PayManager.card_injection(card_name, card_balance)

    # TODO 카드 반환 기능
    # 카드 반환 이벤트가 발생할 경우
    # manager_wallte에서 Temp_Card를 초기화
    def card_return(self, choice):
        # 이후 통계에 사용될 변수
        card_name = choice.replace(":", "").split()[0]
        self.wallet['Card'].return_card()

    def init_card(self):
        self.wallet['Card'].return_card()