class Card:
    def __init__(self):
        self.__card_list = dict()

    def add_card(self):
        new_card = {
            "카드명": "",
            "잔액": 0
        }
        # TODO Management System에서 등록가능 카드 목록 만들기
