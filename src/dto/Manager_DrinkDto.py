from tkinter import *
# from tkinter.messagebox import *
import customtkinter
import json
from PIL import ImageTk
from PIL import Image

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from controller import VMController
from controller import ManagerController


# 구매 가능 상태 텍스트 설정
class Manager_DrinkDto:
    # 생성자
    # (생성할 Frame, 음료명, 현재 재고, 판매상태, 고유인덱스)
    def __init__(self, window, label, stock, state, price, content_id):
        # 처음 시작시 화폐, 카드 투입 전이기 때문에 구매 불가
        self.vmController = VMController.VMController()
        self.managerController = ManagerController.ManagerController()
        self.state = "판매불가"
        # self.state = state
        self.imgSize = 64
        self.content_id = content_id

        img = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/drink.png"),
                                     dark_image=Image.open(r"/Users/mac/Vending-Machine/images/drink.png"),
                                     size=(64, 64))
        img_cola = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/cola.png"),
                                          dark_image=Image.open(r"/Users/mac/Vending-Machine/images/cola.png"),
                                          size=(64, 64))
        img_water = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/water.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/water.png"),
                                           size=(64, 64))
        img_cider = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/cider.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/cider.png"),
                                           size=(64, 64))
        img_mongo = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/mongo.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/mongo.png"),
                                           size=(64, 64))
        img_coffee = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/coffee.png"),
                                            dark_image=Image.open(r"/Users/mac/Vending-Machine/images/coffee.png"),
                                            size=(64, 64))
        img_lemon = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/lemon.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/lemon.png"),
                                           size=(64, 64))
        img_choco = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/choco.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/choco.png"),
                                           size=(64, 64))
        img_apple = customtkinter.CTkImage(light_image=Image.open(r"/Users/mac/Vending-Machine/images/apple.png"),
                                           dark_image=Image.open(r"/Users/mac/Vending-Machine/images/apple.png"),
                                           size=(64, 64))
        img_energy_drink = customtkinter.CTkImage(
            light_image=Image.open(r"/Users/mac/Vending-Machine/images/energy-drink.png"),
            dark_image=Image.open(r"/Users/mac/Vending-Machine/images/energy-drink.png"),
            size=(64, 64))

        self.select_img = ""
        if label == '물':
            self.select_img = img_water
        elif '콜라' in label:
            self.select_img = img_cola
        elif '사이다' in label or '트레비' in label:
            self.select_img = img_cider
        elif '망고' in label or '립톤' in label:
            self.select_img = img_mongo
        elif '핫식스' in label:
            self.select_img = img_energy_drink
        elif '레몬' in label:
            self.select_img = img_lemon
        elif '가나' in label:
            self.select_img = img_choco
        elif '사과' in label or '게토레이' in label or '마운틴듀오' in label or '코코 포도' in label:
            self.select_img = img_apple
        elif '콘트라베이스' in label or '레쓰비' in label:
            self.select_img = img_coffee
        else:
            self.select_img = img

        self.canvas = customtkinter.CTkLabel(window, image=self.select_img, text="")
        self.state_btn = customtkinter.CTkButton(window, fg_color="transparent", border_width=2, text_color=("green", "green"))
        # self.state_btn.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label = customtkinter.CTkLabel(
            window,
            text=label,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            height=1
        )
        self.label_text = label
        # StringVar에 바로 값 초기화시 출력할 Frame이 설정되어있지 않아 오류 발생
        # textvariable에 할당 후 값 초기화
        self.stock_box_text = StringVar()
        self.stock_box = Spinbox(window, textvariable=self.stock_box_text, from_=0, to=30, validate='none', width=11,
                                 state='readonly', increment=1)
        # StringVar 값 초기화
        self.stock_box_text.set(stock)
        # 음료당 가격
        self.drink_price = price
        self.price_label = customtkinter.CTkLabel(
            window,
            text=f"{price}원",
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        # Content 고유 ID
        self.id = content_id
        self.stock = stock
        # 판매 상태값 초기화
        self.state_init(state, stock)

    def __int__(self):
        return self.id

    # def open_input_dialog_event(self):
    #     dialog = customtkinter.CTkInputDialog(text="추가할 재고의 개수를 입력해주세요.", title="재고 구매")
    #     input_val = dialog.get_input()
    #     # 재고 추가 입력값 유효성 확인
    #     if not input_val.isdigit() and int(input_val) <= 0:
    #         print("ffff")
    #         return
    #     # 계좌 잔고 불러오기
    #     managerBank = self.managerController.findManagerBank()
    #     # 잔고 금액이 충분한지 확인
    #     if int(input_val) * int(self.drink_price / 2) <= managerBank:
    #         # 구매 가능할 경우 Manager Bank에서 차감
    #         managerBank -= int(input_val) * int(self.drink_price / 2)
    #         self.managerController.decreaseManagerBank(managerBank)
    #         # 재고 추가
    #         self.managerController.increaseDrink(self.content_id, int(input_val))
    #         # 로고 라벨 수정
    #         self.stock += int(input_val)
    #         self.label.configure(text=f"{self.stock}개")
    #         print("추가 구매 개수:", input_val)

    def buy_flag(self):
        self.drink_buy_event()

    def drink_buy_event(self, drink_name, drink_price, user_seq):
        # TODO 구매 기능 추가
        self.vmController.drink_buy(drink_name, drink_price, user_seq)

    # 구매시 재고 수정 이후 판매 상태 수정 함수 (초기화 & 데이터 파일 수정)
    def state_init(self, state, amount):
        if state == "판매불가" or amount <= 0:
            self.state_btn.configure(
                text_color=("red", "red"),
                text_color_disabled=("red", "red"),
                text="○        구매불가",
                state='disabled'
            )
        elif state == "판매중":
            self.state_btn.configure(
                text="●        구매가능",
                text_color=("green", "green"),
                text_color_disabled=("green", "green"),
                state='normal'
            )
    # 재고 수정 함수
    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)

    def open_input_dialog_event(self, idx, content_id):
        dialog = customtkinter.CTkInputDialog(text="추가할 재고의 개수를 입력해주세요.", title="재고 구매")
        input_val = dialog.get_input()
        # 재고 추가 입력값 유효성 확인
        if not input_val.isdigit() or int(input_val) <= 0:
            return
        # 계좌 잔고 불러오기
        managerBank = self.managerController.findManagerBank()
        # 잔고 금액이 충분한지 확인
        if int(input_val) * int(self.drink_price / 2) <= managerBank:
            # 구매 가능할 경우 Manager Bank에서 차감
            print(f"계좌 잔액: {managerBank}(-{int(input_val) * int(self.drink_price / 2)})    ->    {managerBank - int(input_val) * int(self.drink_price / 2)}")
            managerBank -= int(input_val) * int(self.drink_price / 2)
            self.managerController.decreaseManagerBank(int(input_val) * int(self.drink_price / 2))
            # 재고 추가
            self.managerController.increaseDrink(content_id, input_val)
            # 로고 라벨 수정
            self.stock += int(input_val)
            self.state_btn.configure(text=f"{self.stock}개")
            print(f"음료명: {self.label_text},\t\t추가 구매 개수: {input_val}")
