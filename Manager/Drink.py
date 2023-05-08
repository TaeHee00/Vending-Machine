from tkinter import *


class Drink:

    # TODO state매개변수 추가 후 파일 read후 판매 상태를 초기값으로 설정
    def __init__(self, window, label, stock, state, content_id):
        self.state = state
        self.imgSize = 64
        self.canvas = Canvas(window, width=self.imgSize, height=self.imgSize, highlightthickness=0)
        self.state_btn = Button(window, text="●          판매중", width=9, fg='green', activebackground='gray', command=lambda: self.state_change(self.state))
        self.label = Label(window, text=label, font="Helvetica 12 bold")
        self.stock_box_text = StringVar()
        self.stock_box = Spinbox(window, textvariable=self.stock_box_text, from_=0, to=30, validate='none', width=11, state='readonly', increment=1)
        self.state_init(state)
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
        if state == "판매중":
            self.state_btn.config(text="●          판매중", fg='green', activebackground='gray')
        elif state == "판매불가":
            self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray')

    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)
