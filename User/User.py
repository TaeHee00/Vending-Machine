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
