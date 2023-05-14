from tkinter import *
import customtkinter
import json
from PIL import ImageTk
from PIL import Image

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from controller import VMController


# 구매 가능 상태 텍스트 설정
class VM_DrinkDto:

    # 생성자
    # (생성할 Frame, 음료명, 현재 재고, 판매상태, 고유인덱스)
    def __init__(self, window, label, stock, state, price, content_id):
        # 처음 시작시 화폐, 카드 투입 전이기 때문에 구매 불가
        self.vmController = VMController.VMController()
        self.state = "판매불가"
        # self.state = state
        self.imgSize = 64

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
        self.state_btn = Button(window, text="●          판매중", width=9, fg='green', activebackground='gray')
        self.label = Label(window, text=label, font="Helvetica 12 bold")
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
        self.price_label = Label(window, text=f"{price}원", font="Helvetica 12 bold")
        # Content 고유 ID
        self.id = content_id
        self.stock = stock
        # 판매 상태값 초기화
        self.state_init(state, stock)

    def __int__(self):
        return self.id

    def buy_flag(self):
        self.drink_buy_event()

    def drink_buy_event(self, drink_name, drink_price, user_seq):
        # TODO 구매 기능 추가
        self.vmController.drink_buy(drink_name, drink_price, user_seq)

    # 구매시 재고 수정 이후 판매 상태 수정 함수
    def state_change(self, state):
        if state == "판매중":
            self.state = "판매불가"
            self.state_btn.config(text="○        구매불가", fg='red', activebackground='gray')
        elif state == "판매불가":
            self.state = "판매중"
            self.state_btn.config(text="●        구매가능", fg='green', activebackground='gray')

    # 구매시 재고 수정 이후 판매 상태 수정 함수 (초기화 & 데이터 파일 수정)
    def state_init(self, state, amount):
        if state == "판매불가" or amount <= 0:
            self.state_btn.config(text="○        구매불가", fg='red', activebackground='gray', disabledforeground='red',
                                  bg='gray')
            self.state_btn['state'] = 'disabled'
        elif state == "판매중":
            self.state_btn.config(text="●        구매가능", fg='green', activebackground='gray')
            self.state_btn['state'] = 'normal'

    # 재고 수정 함수
    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)
