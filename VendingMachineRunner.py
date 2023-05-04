from tkinter import *
from tkinter.ttk import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json


vm_window = Tk()
vm_window.title("자판기")
# 창의 초기 생성위치 설정
vm_window.config(padx=30, pady=20)
vm_window.geometry("+500+0")

# 가로 줄에 진열할 상품의 개수
row_limit = 6

# Canvas 내부에 들어갈 임시 이미지 크기
imgSize = 64
img = ImageTk.PhotoImage(file="images/drink.png")
img_cola = ImageTk.PhotoImage(file="images/cola.png")
img_water = ImageTk.PhotoImage(file="images/water.png")
img_cider = ImageTk.PhotoImage(file="images/cider.png")
img_mongo = ImageTk.PhotoImage(file="images/mongo.png")
img_coffee = ImageTk.PhotoImage(file="images/coffee.png")
img_lemon = ImageTk.PhotoImage(file="images/lemon.png")
img_choco = ImageTk.PhotoImage(file="images/choco.png")
img_apple = ImageTk.PhotoImage(file="images/apple.png")
img_energy_drink = ImageTk.PhotoImage(file="images/energy-drink.png")

# 음료가 추가될 경우 계속하여 객체를 만들어주어야 하기 때문에 관리의 편의성을 위해서
# 리스트 내부에 객체를 저장하여 사용
canvas_list = list()
label_list = list()
btn_list = list()

# drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
with open("drink_list.json", "r") as file:
    drink_list = json.load(file)

    # 음료 객체의 자리 배치에 사용하는 변수
    column_cnt = 0
    row_cnt = 0
    for drink in drink_list:
        label_list.append(Label(text=drink, font="Helvetica 12 bold"))
        canvas_list.append(Canvas(width=imgSize, height=imgSize, highlightthickness=0))
        # Canvas가 이미지 배치를 image의 중앙을 기준으로 배치함
        # imgSize / 2로 정렬
        if drink == '물':
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_water)
        elif '콜라' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_cola)
        elif '사이다' in drink or '트레비' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_cider)
        elif '망고' in drink or '립톤' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_mongo)
        elif '핫식스' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_energy_drink)
        elif '레몬' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_lemon)
        elif '가나' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_choco)
        elif '사과' in drink or '게토레이' in drink or '마운틴듀오' in drink or '코코 포도' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_apple)
        elif '콘트라베이스' in drink or '레쓰비' in drink:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img_coffee)
        else:
            canvas_list[-1].create_image(imgSize / 2, imgSize / 2, image=img)
        # 음료 재고에 따라 구매가능, 구매불가 판별
        if drink_list[drink]['재고'] > 0:
            btn_list.append(Button(text="●        구매가능", fg='green', focusthickness=0, activebackground='gray'))
            btn_list[-1]['state'] = 'normal'
        else:
            btn_list.append(Button(text="○        구매불가", disabledforeground='red', bg='gray'))
            btn_list[-1]['state'] = 'disabled'

        # 객체 생성
        canvas_list[-1].grid(row=row_cnt, column=column_cnt)
        label_list[-1].grid(row=row_cnt + 1, column=column_cnt)
        btn_list[-1].grid(row=row_cnt + 2, column=column_cnt, padx=15)

        column_cnt += 1
        Label(text=" ").grid(row=row_cnt + 3, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 4, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 5, column=column_cnt)
        if column_cnt % row_limit == 0:
            # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
            column_cnt = 0
            row_cnt += 6

# 자판기 사용 유저의 지갑
# cash: 현금 저장용
# card: 카드 저장용
user_wallet = {
    "cash": {
        5000: 0,
        1000: 0,
        500: 0,
        100: 0
    },
    "card": {

    }
}
machine_amount = 0

# 자판기에 투입된 금액 표시
machine_amount_label = Label(text=f"투입된 금액:\t{machine_amount}원", font="Helvetica 16 bold")
# 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
machine_amount_label.grid(row=99, column=abs(row_limit - 2), columnspan=3)

Label(text=" ").grid(row=100, column=column_cnt)
user_cash_tuple = tuple([
    f"5000원: {user_wallet['cash'][5000]}개",
    f"1000원: {user_wallet['cash'][1000]}개",
    f"500원: {user_wallet['cash'][500]}개",
    f"100원: {user_wallet['cash'][100]}개"
])
# TODO 이후 User Class의 Wallte Class의 Card Class에서 받아올것.
# 임시 데이터
user_card_tuple = tuple([
    f"농협카드: {125000}원",
    f"현대카드: {900000}원",
    f"IBK카드: {6200000}원"
])

amount_increase_combo = Combobox(vm_window, width=15, state='readonly')
amount_increase_combo['value'] = user_cash_tuple
amount_increase_combo.current(0)
amount_increase_combo.grid(row=101, column=abs(row_limit - 2))
amount_increase_btn = Button(text="현금 투입", focusthickness=0, activebackground='gray', width=160)
amount_increase_btn.grid(row=102, column=abs(row_limit - 2))

cash_increase_combo = Combobox(vm_window, width=15, state='readonly')
cash_increase_combo['value'] = user_card_tuple
cash_increase_combo.current(0)
cash_increase_combo.grid(row=101, column=abs(row_limit - 1))
amount_increase_btn = Button(text="카드 투입", focusthickness=0, activebackground='gray', width=160)
amount_increase_btn.grid(row=102, column=abs(row_limit - 1))

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
