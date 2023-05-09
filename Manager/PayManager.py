import json


# 카드 내용을 가져온 후 카드명과 카드의 잔액을 임시로 파일에 저장
def card_injection(card_name, card_balance):
    # 상대경로로 참조해도 되지만 User폴더->Manager폴더->데이터파일 방식으로 접근하는 경우 파일을 못찾는 경우 발생
    # 절대경로를 사용하여 해결
    with open("/Users/mac/Vending-Machine/Manager/manager_wallet.json", "r") as file:
        wallet_data = json.load(file)
    wallet_data['Temp_Card']['카드명'] = card_name
    wallet_data['Temp_Card']['잔액'] = card_balance

    with open("/Users/mac/Vending-Machine/Manager/manager_wallet.json", 'w') as file:
        json.dump(wallet_data, file, indent=4, ensure_ascii=False)
