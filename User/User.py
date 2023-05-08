class User:

    def __init__(self):
        self.__wallet = {
            "cash": {
                5000: 0,
                1000: 0,
                500: 0,
                100: 0
            },
            "card": {

            }
        }

        self.__bag = dict()

    def get_cash(self):
        return self.__wallet["cash"]

    def get_card(self):
        return self.__wallet["card"]
