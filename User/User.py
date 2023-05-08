import Cash
import Card


class User:

    def __init__(self):
        self.wallet = {
            "cash": Cash.Cash(),
            "card": Card.Card()
        }

        self.bag = dict()

