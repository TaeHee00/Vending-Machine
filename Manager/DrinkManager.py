from tkinter import *
from tkinter.ttk import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json
import Drink


class DrinkManager:
    window = Tk()
    window.title("Drink Management")
    window.config(padx=15, pady=15)
    window.geometry("+400+0")
    window.resizable(False, False)

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
    with open("drink_list.json", "r") as file:
        drink_list = json.load(file)

        # 음료 객체의 자리 배치에 사용하는 변수
        column_cnt = 0
        row_cnt = 0
        idx = 0
        for drink in drink_list:
            drink_content.append(Drink.Drink(window, drink, drink_list[drink]['재고'], drink_list[drink]['상태'], idx))

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
            drink_content[idx].stock_box.grid(row=row_cnt + 2, column=column_cnt, padx=15)
            drink_content[idx].state_btn.grid(row=row_cnt + 3, column=column_cnt)

            column_cnt += 1
            Label(text=" ").grid(row=row_cnt + 4, column=column_cnt)
            Label(text=" ").grid(row=row_cnt + 5, column=column_cnt)
            Label(text=" ").grid(row=row_cnt + 6, column=column_cnt)
            if column_cnt % row_limit == 0:
                # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
                column_cnt = 0
                row_cnt += 6
            idx += 1

    Label(text="음료 재고 관리중...", font="Helvetica 25 bold", foreground="red").grid(row=99, column=1, rowspan=3)
    # 자판기 사용 유저의 지갑
    # cash: 현금 저장용
    # card: 카드 저장용
    user_wallet = {
        "cash": {
            5000: 15,
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
        f"농협카드: {75000}원",
        f"현대카드: {900000}원",
        f"IBK카드: {6200000}원"
    ])

    amount_increase_combo = Combobox(window, width=15, state='readonly')
    amount_increase_combo['value'] = user_cash_tuple
    amount_increase_combo.current(0)
    amount_increase_combo.grid(row=101, column=abs(row_limit - 2))
    amount_increase_btn = Button(text="현금 투입", focusthickness=0, activebackground='gray', width=160)
    amount_increase_btn.grid(row=102, column=abs(row_limit - 2))

    cash_increase_combo = Combobox(window, width=15, state='readonly')
    cash_increase_combo['value'] = user_card_tuple
    cash_increase_combo.current(0)
    cash_increase_combo.grid(row=101, column=abs(row_limit - 1))
    amount_increase_btn = Button(text="카드 투입", focusthickness=0, activebackground='gray', width=160)
    amount_increase_btn.grid(row=102, column=abs(row_limit - 1))

    window.mainloop()
