import json


# 카드 내용을 가져온 후 카드명과 카드의 잔액을 임시로 파일에 저장
def card_injection(card_name, card_balance):
    with open("manager_wallet.json", "r") as file:
        wallet_data = json.load(file)
    wallet_data['Temp_Card']['카드명'] = card_name
    wallet_data['Temp_Card']['잔액'] = card_balance

    with open("manager_wallet.json", 'w') as file:
        json.dump(wallet_data, file, indent=4, ensure_ascii=False)
