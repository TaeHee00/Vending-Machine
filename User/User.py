import json
import Card
import Cash


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
        print(choice)

    # TODO 현금 반환  기능
    def cash_return(self):
        pass

    # TODO 카드 투입 기능
    def card_injection(self, choice):
        print(choice)

    # TODO 카드 반환 기능
    def card_return(self):
        pass