from CustomException import *
import json


class Cash:

    def __init__(self):
        with open("user_wallet.json", "r") as file:
            self.Cash = json.load(file)['Cash']

    def set_cash(self, money_type, how_much):
        if how_much >= 0:
            if money_type == "5000":
                self.Cash["5000"] = how_much
            elif money_type == "1000":
                self.Cash["1000"] = how_much
            elif money_type == "500":
                self.Cash["500"] = how_much
            elif money_type == "100":
                self.Cash["100"] = how_much

    def total_money(self):
        # TODO 가지고 있는 지폐를 금액으로 환산하여 값을 리턴
        total = 0
        total += self.Cash["5000"] * 5000
        total += self.Cash["1000"] * 1000
        total += self.Cash["500"] * 500
        total += self.Cash["100"] * 100
        return total
