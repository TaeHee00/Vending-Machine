import json


class Card:
    def __init__(self):
        with open("user_wallet.json", "r") as file:
            self.Card = json.load(file)['Card']

    def add_card(self, card_name, balance):
        new_card = {
            "잔액": balance
        }
        self.card_list[card_name] = new_card
        # TODO Management System에서 등록가능 카드 목록 만들기

    def get_balance(self, card_name):
        card_name = card_name.replace(":", "").split()[0]
        with open("user_wallet.json", "r") as file:
            self.Card = json.load(file)['Card']
        return self.Card[card_name]

    def return_card(self):
        with open("/Users/mac/Vending-Machine/Manager/manager_wallet.json", "r") as file:
            wallte_data = json.load(file)
        wallte_data['Temp_Card']['카드명'] = ""
        wallte_data['Temp_Card']['잔액'] = 0

        with open("/Users/mac/Vending-Machine/Manager/manager_wallet.json", "w") as file:
            json.dump(wallte_data, file, indent=4, ensure_ascii=False)
