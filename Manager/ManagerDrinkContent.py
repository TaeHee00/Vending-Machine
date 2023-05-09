from tkinter import *
import json


class ManagerDrinkContent:
    # TODO Interface에서 음료당 가격 보여주는 기능 추가
    # TODO 가격 수정 기능 추가
    # 생성자
    # (생성할 Frame, 음료명, 현재 재고, 판매상태, 고유인덱스)
    def __init__(self, window, label, stock, state, content_id):
        self.state = state
        self.imgSize = 64
        self.canvas = Canvas(window, width=self.imgSize, height=self.imgSize, highlightthickness=0)
        self.state_btn = Button(window, text="●          판매중", width=9, fg='green', activebackground='gray', command=lambda: self.state_change(self.state))
        self.label = Label(window, text=label, font="Helvetica 12 bold")
        self.label_text = label
        # StringVar에 바로 값 초기화시 출력할 Frame이 설정되어있지 않아 오류 발생
        # textvariable에 할당 후 값 초기화
        self.stock_box_text = StringVar()
        self.stock_box = Spinbox(window, textvariable=self.stock_box_text, from_=0, to=30, validate='none', width=11, state='readonly', increment=1)
        # StringVar 값 초기화
        self.state_init(state)
        # 판매 상태값 초기화
        self.stock_box_text.set(stock)
        # Content 고유 ID
        self.id = content_id

    def __int__(self):
        return self.id

    # Content 하단에 판매 상태 변경 버튼 클릭 이벤트 함수
    # 판매중 <--> 판매불가 토글 설정
    def state_change(self, state):
        if state == "판매중":
            self.state = "판매불가"
            self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray')
        elif state == "판매불가":
            self.state = "판매중"
            self.state_btn.config(text="●          판매중", fg='green', activebackground='gray')

    # 초기 판매 상태 설정 함수
    # 재고 부족에 따른 판매 가능 옵션을 배제하기 위해 사용
    # 재고가 없을 경우 판매불가 상태 고정 + 판매중으로 변경 불가능
    def state_init(self, state):
        # 저장되어있는 데이터를 불러와서 상태확인
        with open("./drink_list.json", "r") as file:
            drink_data = json.load(file)
            if state == "판매불가":
                self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray', disabledforeground='red', bg='gray')
            elif state == "판매중":
                self.state_btn.config(text="●          판매중", fg='green', activebackground='gray')
                self.state_btn['state'] = 'normal'

            if drink_data[self.label_text]['재고'] <= 0:
                self.state_btn.config(text="○        판매불가", fg='red', activebackground='gray', disabledforeground='red', bg='gray')
                # 재고가 없을 경우 강제 상태 변경
                drink_data[self.label_text]['상태'] = "판매불가"
                # 재고가 없을 경우 판매 상태를 변경하지 못하도록 버튼 상태를 disabled
                self.state_btn['state'] = 'disabled'

        # 데이터 업데이트
        with open("drink_list.json", 'w') as file:
            json.dump(drink_data, file, indent=4, ensure_ascii=False)

    # 재고 수정 함수
    def set_stock_box(self, text):
        # TODO 유효성 검사
        self.stock_box_text.set(text)
