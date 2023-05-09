from tkinter import *
from tkinter.ttk import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json
import UserDrinkContent
import User


vm_window = Tk()
vm_window.title("자판기")
# 창의 초기 생성위치 설정
vm_window.config(padx=30, pady=20)
vm_window.geometry("+500+0")
vm_window.resizable(False, False)

# 가로 줄에 진열할 상품의 개수
row_limit = 6

# Canvas 내부에 들어갈 임시 이미지 크기
imgSize = 64
img = ImageTk.PhotoImage(file="../images/drink.png")
img_cola = ImageTk.PhotoImage(file="../images/cola.png")
img_water = ImageTk.PhotoImage(file="../images/water.png")
img_cider = ImageTk.PhotoImage(file="../images/cider.png")
img_mongo = ImageTk.PhotoImage(file="../images/mongo.png")
img_coffee = ImageTk.PhotoImage(file="../images/coffee.png")
img_lemon = ImageTk.PhotoImage(file="../images/lemon.png")
img_choco = ImageTk.PhotoImage(file="../images/choco.png")
img_apple = ImageTk.PhotoImage(file="../images/apple.png")
img_energy_drink = ImageTk.PhotoImage(file="../images/energy-drink.png")

# 음료가 추가될 경우 계속하여 객체를 만들어주어야 하기 때문에 관리의 편의성을 위해서
# 리스트 내부에 객체를 저장하여 사용
drink_content = list()

# drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
with open("../Manager/drink_list.json", "r") as file:
    drink_list = json.load(file)

    # 음료 객체의 자리 배치에 사용하는 변수
    column_cnt = 0
    row_cnt = 0
    idx = 0
    for drink in drink_list:
        drink_content.append(UserDrinkContent.UserDrinkContent(vm_window, drink, drink_list[drink]['재고'], drink_list[drink]['상태'], drink_list[drink]['가격'], idx))

        if drink_content[idx].label == '물':
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_water)
        elif '콜라' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_cola)
        elif '사이다' in drink or '트레비' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_cider)
        elif '망고' in drink or '립톤' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_mongo)
        elif '핫식스' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_energy_drink)
        elif '레몬' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_lemon)
        elif '가나' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_choco)
        elif '사과' in drink or '게토레이' in drink or '마운틴듀오' in drink or '코코 포도' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_apple)
        elif '콘트라베이스' in drink or '레쓰비' in drink:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_coffee)
        else:
            drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img)

        # 객체 생성
        drink_content[idx].canvas.grid(row=row_cnt, column=column_cnt)
        drink_content[idx].label.grid(row=row_cnt + 1, column=column_cnt)
        drink_content[idx].price_label.grid(row=row_cnt + 2, column=column_cnt)
        drink_content[idx].state_btn.grid(row=row_cnt + 3, column=column_cnt, padx=15)

        column_cnt += 1
        Label(text=" ").grid(row=row_cnt + 4, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 5, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 6, column=column_cnt)
        if column_cnt % row_limit == 0:
            # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
            column_cnt = 0
            row_cnt += 6
        idx += 1

# 자판기 사용 유저의 지갑
# cash: 현금 저장용
# card: 카드 저장용
user = User.User()
# 자판기 실행시 manager_wallte['Temp_Card'] 내용 초기화
user.init_card()
machine_amount = 0

# 자판기에 투입된 금액 표시
machine_amount_label = Label(text=f"투입된 금액:\t{machine_amount}원", font="Helvetica 16 bold")
# 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
machine_amount_label.grid(row=99, column=abs(row_limit - 2), columnspan=3)

Label(text=" ").grid(row=100, column=column_cnt)
user_cash_tuple = tuple([
    f"5000원: {user.wallet['Cash'].Cash['5000']}개",
    f"1000원: {user.wallet['Cash'].Cash['1000']}개",
    f"500원: {user.wallet['Cash'].Cash['500']}개",
    f"100원: {user.wallet['Cash'].Cash['100']}개"
])

with open("user_wallet.json", 'r') as file:
    card_data = json.load(file)['Card']
    card_list = list()
    for card in card_data:
        card_list.append(f"{card}: {card_data[card]}원")
    user_card_tuple = tuple(card_list)


# TODO 화폐, 카드 투입 전 구매 버튼 비활성화

# 현금 결제를 위한 Drop-down 옵션
# 자판기와 동일한 동작을 위해 화폐는 하나씩 투입하도록 설정
amount_increase_combo = Combobox(vm_window, width=15, state='readonly')
amount_increase_combo['value'] = user_cash_tuple
amount_increase_combo.current(0)
amount_increase_combo.grid(row=101, column=abs(row_limit - 2))
amount_increase_btn = Button(text="현금 투입", focusthickness=0, activebackground='gray', width=160,
                             command=lambda: user.cash_injection(amount_increase_combo.get()))
amount_increase_btn.grid(row=102, column=abs(row_limit - 2))

# 카드 결제를 위한 Drop-down 옵션
# 카드를 투입 후 반환 전까지 카드의 잔액을 사용하여 결제
cash_increase_combo = Combobox(vm_window, width=15, state='readonly')
cash_increase_combo['value'] = user_card_tuple
cash_increase_combo.current(0)
cash_increase_combo.grid(row=101, column=abs(row_limit - 1))
amount_increase_btn = Button(text="카드 투입", focusthickness=0, activebackground='gray', width=160,
                             command=lambda: card_injection_event())
amount_increase_btn.grid(row=102, column=abs(row_limit - 1))


# TODO 카드 삽입,제거시 투입된 금액 Label 변경
# TODO 카드 삽입시 잔액에 따라 구매 가능한 음료만 판매 상태 변경
# TODO 구매시 카드 잔액 실시간 업데이트
# TODO 구매시 user_bag에 음료명: 개수 추가
# TODO Manager 통계에서 판매 수익 및 판매 음료 추가
def card_injection_event():
    # 카드 삽입
    if amount_increase_btn['text'] == "카드 투입":
        amount_increase_btn['text'] = f"{cash_increase_combo.get().replace(':', '').split()[0]} 투입됨"
        amount_increase_btn['fg'] = "green"
        user.card_injection(cash_increase_combo.get())

        for _drink in drink_content:
            # TODO 조건 재확인 필요
            if drink_list[_drink.label_text]['재고'] <= 0 or drink_list[_drink.label_text]['가격'] > user.wallet['Card'].get_balance(cash_increase_combo.get()):
                _drink.state_btn['text'] = "○        구매불가"
                _drink.state_btn['fg'] = "red"
                _drink.state_btn['state'] = "disabled"
                # print(_drink.state, drink_list[_drink.label_text]['재고'], drink_list[_drink.label_text]['가격'], user.wallet['Card'].get_balance(cash_increase_combo.get()))
            else:
                _drink.state_btn['text'] = "●        구매가능"
                _drink.state_btn['fg'] = "green"
                _drink.state_btn['state'] = "normal"
    else:
        # 카드 제거
        # TODO 카드 총 사용 내역 기능 추가 예정
        amount_increase_btn['text'] = "카드 투입"
        amount_increase_btn['fg'] = "black"
        user.card_return(cash_increase_combo.get())

        for _drink in drink_content:
            _drink.state_btn['text'] = "○        구매불가"
            _drink.state_btn['state'] = "disabled"


vm_window.mainloop()

# try:
#     with open("drink_list.json", "r") as drink_list_file:
#         data = json.load(drink_list_file)
#
# except FileNotFoundError:
#     with open("drink_list.json", "w") as drink_list_file:
#         data = {
#
#         }
#         json.dump(data, drink_list_file, indent=4)
#
# else:
#     while True:
#         drink_name = input("음료수 이름을 입력하세요: ")
#         if drink_name == "break":
#             break
#         drink_price = int(input("음료수 가격을 입력하세요: "))
#         drink_num = int(input("음료수 재고를 입력하세요: "))
#         new_data = {
#             drink_name: {
#                 "가격": drink_price,
#                 "재고": drink_num
#             }
#         }
#         data.update(new_data)
#         print("\n")
#
#         with open("drink_list.json", "w") as drink_list_file:
#             json.dump(data, drink_list_file, indent=4, ensure_ascii=False)
