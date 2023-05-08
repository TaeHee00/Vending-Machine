from CustomException import *


class Cash:

    def __init__(self):
        self.__Cash = {
            5000: 0,
            1000: 0,
            500: 0,
            100: 0
        }

    def set_cash(self, money_type, how_much):
        if money_type == 5000 or money_type == 1000 or money_type == 500 or money_type == 100:
            if (type(how_much) == int or how_much.isdigit()) and how_much >= 0:
                if money_type == 5000:
                    self.__Cash[5000] = how_much
                elif money_type == 1000:
                    self.__Cash[1000] = how_much
                elif money_type == 500:
                    self.__Cash[500] = how_much
                elif money_type == 100:
                    self.__Cash[100] = how_much
                else:
                    raise ArgumentException("Cash.set_cash argument exception")
        else:
            raise ArgumentException("Cash.set_cash argument exception")

    def total_money(self):
        # TODO 가지고 있는 지폐를 금액으로 환산하여 값을 리턴
        total = 0
        total += self.__Cash[5000] * 5000
        total += self.__Cash[1000] * 1000
        total += self.__Cash[500] * 500
        total += self.__Cash[100] * 100
        return total
