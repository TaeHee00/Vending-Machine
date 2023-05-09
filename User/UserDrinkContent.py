from tkinter import *
import json


class UserDrinkContent:

    # 생성자
    # (생성할 Frame, 음료명, 현재 재고, 판매상태, 고유인덱스)
    def __init__(self, window, label, stock, state, content_id):
        self.state = state
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
        # 판매 상태값 초기화
        self.state_init(state)
        # Content 고유 ID
        self.id = content_id

    def __int__(self):
        return self.id

    # Content 하단에 판매 상태 변경 버튼 클릭 이벤트 함수
    # 판매중 <--> 판매불가 토글 설정
    def state_change(self, state):
        if state == "판매중":
            self.state = "판매불가"
            self.state_btn.config(text="○        구매불가", fg='red', activebackground='gray')
        elif state == "판매불가":
            self.state = "판매중"
            self.state_btn.config(text="●        구매가능", fg='green', activebackground='gray')

    # 초기 판매 상태 설정 함수
    # 재고 부족에 따른 판매 가능 옵션을 배제하기 위해 사용
    # 재고가 없을 경우 판매불가 상태 고정 + 판매중으로 변경 불가능
    def state_init(self, state):
        with open("./Manager/drink_list.json", "r") as file:
            drink_list = json.load(file)
            if state == "판매불가" or drink_list[self.label_text]['재고'] <= 0:
                self.state_btn.config(text="○        구매불가", fg='red', activebackground='gray', disabledforeground='red', bg='gray')
                self.state_btn['state'] = 'disabled'
            elif state == "판매중":
                self.state_btn.config(text="●        구매가능", fg='green', activebackground='gray')
                self.state_btn['state'] = 'normal'

    # 재고 수정 함수
    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)
