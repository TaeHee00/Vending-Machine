class Card:
    def __init__(self):
        self.card_list = dict()

    def add_card(self, card_name, balance):
        new_card = {
            "잔액": balance
        }
        self.card_list[card_name] = new_card
        # TODO Management System에서 등록가능 카드 목록 만들기
