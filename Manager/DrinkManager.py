from tkinter import *
from tkinter.ttk import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
from tkinter.messagebox import *
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json
import ManagerDrinkContent
import copy


class DrinkManager:

    def __init__(self):
        self.window = Tk()
        self.window.title("Drink Management")
        self.window.config(padx=15, pady=15)
        self.window.geometry("+400+0")
        self.window.resizable(False, False)
        # 음료가 추가될 경우 계속하여 객체를 만들어주어야 하기 때문에 관리의 편의성을 위해서
        # 리스트 내부에 객체를 저장하여 사용
        self.drink_content = list()

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

        # drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
        with open("drink_list.json", "r") as file:
            drink_list = json.load(file)

            # 음료 객체의 자리 배치에 사용하는 변수
            column_cnt = 0
            row_cnt = 0
            idx = 0
            for drink in drink_list:
                self.drink_content.append(ManagerDrinkContent.ManagerDrinkContent(self.window, drink, drink_list[drink]['재고'], drink_list[drink]['상태'], idx))

                if self.drink_content[idx].label == '물':
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_water)
                elif '콜라' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_cola)
                elif '사이다' in drink or '트레비' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_cider)
                elif '망고' in drink or '립톤' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_mongo)
                elif '핫식스' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_energy_drink)
                elif '레몬' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_lemon)
                elif '가나' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_choco)
                elif '사과' in drink or '게토레이' in drink or '마운틴듀오' in drink or '코코 포도' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_apple)
                elif '콘트라베이스' in drink or '레쓰비' in drink:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img_coffee)
                else:
                    self.drink_content[idx].canvas.create_image(imgSize / 2, imgSize / 2, image=img)

                # 객체 생성
                self.drink_content[idx].canvas.grid(row=row_cnt, column=column_cnt)
                self.drink_content[idx].label.grid(row=row_cnt + 1, column=column_cnt)
                self.drink_content[idx].stock_box.grid(row=row_cnt + 2, column=column_cnt, padx=15)
                self.drink_content[idx].state_btn.grid(row=row_cnt + 3, column=column_cnt)

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
        total_price = 0

        # 추가할 재고의 총 가격 (각 음료 개당 판매 금액의 50%)
        total_price_label = Label(text=f"재고 추가 금액:\t{total_price}원", font="Helvetica 16 bold")
        # 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
        total_price_label.grid(row=99, column=abs(row_limit - 3), columnspan=3)

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

        stock_buy_btn = Button(text="추가 재고 구매", focusthickness=0, activebackground='gray', width=160)
        stock_buy_btn.grid(row=102, column=abs(row_limit - 3))

        state_set_btn = Button(text="판매 상태 설정", focusthickness=0, activebackground='gray', width=160, command=self.state_setup)
        state_set_btn.grid(row=102, column=abs(row_limit - 2))

        back_btn = Button(text="나가기", focusthickness=0, activebackground='gray', width=160, command=self.back_page)
        back_btn.grid(row=102, column=abs(row_limit - 1))

        self.window.mainloop()

    def back_page(self):
        self.window.destroy()

    def state_setup(self):
        with open("drink_list.json", "r") as file:
            drink_data = json.load(file)
            old_drink_data = copy.deepcopy(drink_data)
            # 진열대에 있는 모든 음료를 가져온다.
            for drink in self.drink_content:

                # 변경된 정보와 관리 데이터 연동
                if drink.state == "판매중":
                    drink_data[drink.label_text]['상태'] = "판매중"
                    drink.state_btn['state'] = 'normal'

                elif drink.state == "판매불가":
                    drink_data[drink.label_text]['상태'] = "판매불가"
                    # 관리 데이터의 재고가 0개 초과 일 경우 버튼을 클릭 가능하게 설정
                    if drink_data[drink.label_text]['재고'] > 0:
                        drink.state_btn['state'] = 'normal'
                    else:
                        drink.state_btn['state'] = 'disabled'

        with open("drink_list.json", 'w') as file:
            json.dump(drink_data, file, indent=4, ensure_ascii=False)

        change_state = ""
        for drink in drink_data:
            if drink_data[drink]['상태'] != old_drink_data[drink]['상태']:
                change_state += f"[ {drink} ]\n{old_drink_data[drink]['상태']}   ->   {drink_data[drink]['상태']}\n\n"

        if change_state == "":
            showinfo("설정 정보", "변경된 판매 상태가 없습니다.")
        else:
            showinfo("설정 정보", f"\n{change_state}판매 상태가 성공적으로 변경되었습니다!")
