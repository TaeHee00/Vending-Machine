from tkinter import *
import json


# TODO 구매 가능 상태 텍스트 설정호
class VM_DrinkDto:

    # 생성자
    # (생성할 Frame, 음료명, 현재 재고, 판매상태, 고유인덱스)
    def __init__(self, window, label, stock, state, price, content_id):
        # 처음 시작시 화폐, 카드 투입 전이기 때문에 구매 불가
        self.state = "판매불가"
        # self.state = state
        self.imgSize = 64
        self.canvas = Canvas(window, width=self.imgSize, height=self.imgSize, highlightthickness=0)
        self.state_btn = Button(window, text="●          판매중", width=9, fg='green', activebackground='gray')
        self.label = Label(window, text=label, font="Helvetica 12 bold")
        self.label_text = label
        # StringVar에 바로 값 초기화시 출력할 Frame이 설정되어있지 않아 오류 발생
        # textvariable에 할당 후 값 초기화
        self.stock_box_text = StringVar()
        self.stock_box = Spinbox(window, textvariable=self.stock_box_text, from_=0, to=30, validate='none', width=11, state='readonly', increment=1)
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
