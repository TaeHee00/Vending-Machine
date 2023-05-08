from tkinter import *
import json


class ManagerDrinkContent:

    # TODO state매개변수 추가 후 파일 read후 판매 상태를 초기값으로 설정
    def __init__(self, window, label, stock, state, content_id):
        self.state = state
        self.imgSize = 64
        self.canvas = Canvas(window, width=self.imgSize, height=self.imgSize, highlightthickness=0)
        self.state_btn = Button(window, text="●          판매중", width=9, fg='green', activebackground='gray', command=lambda: self.state_change(self.state))
        self.label = Label(window, text=label, font="Helvetica 12 bold")
        self.label_text = label
        self.stock_box_text = StringVar()
        self.stock_box = Spinbox(window, textvariable=self.stock_box_text, from_=0, to=30, validate='none', width=11, state='readonly', increment=1)
        self.state_init(state)
        self.stock_box_text.set(stock)
        self.id = content_id

    def __int__(self):
        return self.id

    def state_change(self, state):
        if state == "판매중":
            self.state = "판매불가"
            self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray')
        elif state == "판매불가":
            self.state = "판매중"
            self.state_btn.config(text="●          판매중", fg='green', activebackground='gray')

    def state_init(self, state):
        # TODO 재고가 없을 경우 판매불가로 고정하여 바꾸지 못하도록 설정
        # TODO 재고 추가할 경우 판매 가능으로 변경 가능
        with open("./drink_list.json", "r") as file:
            drink_list = json.load(file)
            if state == "판매불가":
                self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray', disabledforeground='red', bg='gray')
            elif state == "판매중":
                self.state_btn.config(text="●          판매중", fg='green', activebackground='gray')
                self.state_btn['state'] = 'normal'

            if drink_list[self.label_text]['재고'] <= 0:
                self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray', disabledforeground='red', bg='gray')
                self.state_btn['state'] = 'disabled'

    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)
