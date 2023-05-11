from tkinter import *
from tkinter.ttk import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json
from controller import DrinkController
import User

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dto import VM_DrinkDto


# TODO 카드 구매기능 구현
# TODO 구매시 src inventory에 저장하도록 구현
# TODO 구매시 금액 차감후 실시간 정보 변경(카드 정보 수정 및 기타 금액 출력부분 Refrash)

# TODO 화폐 구매기능 구현
# TODO 구매시 잔액 계산 후 나머지돈 Return
# TODO 나머지돈을 화폐 재고에 맞게 Return
# TODO 화폐 재고가 부족할 경우에도 구매 불가능하도록 설정
class UserApplication:

    def __init__(self):
        self.drinkController = DrinkController.DrinkController()
        self.window = Tk()
        self.window.title("자판기")
        # 창의 초기 생성위치 설정
        self.window.config(padx=30, pady=20)
        self.window.geometry("+500+0")
        self.window.resizable(False, False)
        # 가로 줄에 진열할 상품의 개수
        self.row_limit = 6

        # 음료가 추가될 경우 계속하여 객체를 만들어주어야 하기 때문에 관리의 편의성을 위해서
        # 리스트 내부에 객체를 저장하여 사용
        self.drink_content = list()

        # 음료 객체의 자리 배치에 사용하는 변수
        self.column_cnt = 0
        self.row_cnt = 0
        self.idx = 0

        # Canvas 내부에 들어갈 임시 이미지 크기
        self.img_size = 64
        self.img = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/drink.png")
        self.img_cola = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/cola.png")
        self.img_water = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/water.png")
        self.img_cider = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/cider.png")
        self.img_mongo = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/mongo.png")
        self.img_coffee = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/coffee.png")
        self.img_lemon = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/lemon.png")
        self.img_choco = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/choco.png")
        self.img_apple = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/apple.png")
        self.img_energy_drink = ImageTk.PhotoImage(file=r"/Users/mac/Vending-Machine/images/energy-drink.png")


        # drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
        vm_drink_list = self.drinkController.vmDrinkList()
        drink_list = self.drinkController.drinkList()


        for drink in vm_drink_list:
            drinkDto = VM_DrinkDto.VM_DrinkDto(
                window=self.window,
                label=drink_list[drink.getDrinkSeq() - 1].getDrinkName(),
                stock=drink.getAmount(),
                state=drink.getState(),
                price=drink_list[drink.getDrinkSeq() - 1].getDrinkPrice(),
                content_id=drink.getDrinkSeq()
            )
            self.drink_content.append(drinkDto)

            if drinkDto.label_text == '물':
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_water)
            elif '콜라' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_cola)
            elif '사이다' in drinkDto.label_text or '트레비' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_cider)
            elif '망고' in drinkDto.label_text or '립톤' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_mongo)
            elif '핫식스' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_energy_drink)
            elif '레몬' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_lemon)
            elif '가나' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_choco)
            elif '사과' in drinkDto.label_text or '게토레이' in drinkDto.label_text or '마운틴듀오' in drinkDto.label_text or '코코 포도' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_apple)
            elif '콘트라베이스' in drinkDto.label_text or '레쓰비' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img_coffee)
            else:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img)

            # 객체 생성
            self.drink_content[self.idx].canvas.grid(row=self.row_cnt, column=self.column_cnt)
            # self.drink_content[self.idx].canvas.update()
            self.drink_content[self.idx].label.grid(row=self.row_cnt + 1, column=self.column_cnt)
            self.drink_content[self.idx].price_label.grid(row=self.row_cnt + 2, column=self.column_cnt)
            self.drink_content[self.idx].state_btn.grid(row=self.row_cnt + 3, column=self.column_cnt, padx=15)

            self.column_cnt += 1
            Label(text=" ").grid(row=self.row_cnt + 4, column=self.column_cnt)
            Label(text=" ").grid(row=self.row_cnt + 5, column=self.column_cnt)
            Label(text=" ").grid(row=self.row_cnt + 6, column=self.column_cnt)
            if self.column_cnt % self.row_limit == 0:
                # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
                self.column_cnt = 0
                self.row_cnt += 6
            self.idx += 1

        # 자판기 사용 유저의 지갑
        # cash: 현금 저장용
        # card: 카드 저장용
        user = User.User()
        # 자판기 실행시 manager_wallte['Temp_Card'] 내용 초기화
        user.init_card()
        machine_amount = 0

        # 자판기에 투입된 금액 표시
        machine_amount_label = Label(text=f"투입된 금액:\t{machine_amount}원", font="Helvetica 16 bold")
        # 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
        machine_amount_label.grid(row=99, column=abs(self.row_limit - 2), columnspan=3)

        Label(text=" ").grid(row=100, column=self.column_cnt)
        user_cash_tuple = tuple([
            f"5000원: {user.wallet['Cash'].Cash['5000']}개",
            f"1000원: {user.wallet['Cash'].Cash['1000']}개",
            f"500원: {user.wallet['Cash'].Cash['500']}개",
            f"100원: {user.wallet['Cash'].Cash['100']}개"
        ])

        with open("user_wallet.json", 'r') as file:
            card_data = json.load(file)['Card']
            card_list = list()
            for card in card_data:
                card_list.append(f"{card}: {card_data[card]}원")
            user_card_tuple = tuple(card_list)

        # 현금 결제를 위한 Drop-down 옵션
        # 자판기와 동일한 동작을 위해 화폐는 하나씩 투입하도록 설정
        # TODO 화폐 투입 전 구매 버튼 비활성화
        amount_increase_combo = Combobox(self.window, width=15, state='readonly')
        amount_increase_combo['value'] = user_cash_tuple
        amount_increase_combo.current(0)
        amount_increase_combo.grid(row=101, column=abs(self.row_limit - 2))
        amount_increase_btn = Button(text="현금 투입", focusthickness=0, activebackground='gray', width=160,
                                     command=lambda: user.cash_injection(amount_increase_combo.get()))
        amount_increase_btn.grid(row=102, column=abs(self.row_limit - 2))

        # 카드 결제를 위한 Drop-down 옵션
        # 카드를 투입 후 반환 전까지 카드의 잔액을 사용하여 결제
        # 카드 투입 전 구매 버튼 비활성화
        cash_increase_combo = Combobox(self.window, width=15, state='readonly')
        cash_increase_combo['value'] = user_card_tuple
        cash_increase_combo.current(0)
        cash_increase_combo.grid(row=101, column=abs(self.row_limit - 1))
        amount_increase_btn = Button(text="카드 투입", focusthickness=0, activebackground='gray', width=160,
                                     command=lambda: card_injection_event())
        amount_increase_btn.grid(row=102, column=abs(self.row_limit - 1))

        # 카드 삽입시 잔액에 따라 구매 가능한 음료만 판매 상태 변경
        # 카드 삽입,제거시 투입된 금액 Label 변경
        # TODO 구매시 카드 잔액 실시간 업데이트
        # TODO 구매시 user_bag에 음료명: 개수 추가
        # TODO Manager 통계에서 판매 수익 및 판매 음료 추가
        def card_injection_event(self):
            # 카드 삽입
            if amount_increase_btn['text'] == "카드 투입":
                amount_increase_btn['text'] = f"{cash_increase_combo.get().replace(':', '').split()[0]} 투입됨"
                amount_increase_btn['fg'] = "green"
                user.card_injection(cash_increase_combo.get())

                machine_amount_label['text'] = f"카드 잔액:\t{user.wallet['Card'].get_balance(cash_increase_combo.get())}원"

                for _drink in drink_content:
                    # TODO 조건 재확인 필요
                    if drink_list[_drink.label_text]['재고'] <= 0 or drink_list[_drink.label_text]['가격'] > user.wallet[
                        'Card'].get_balance(cash_increase_combo.get()):
                        _drink.state_btn['text'] = "○        구매불가"
                        _drink.state_btn['fg'] = "red"
                        _drink.state_btn['state'] = "disabled"
                        # print(_drink.state, drink_list[_drink.label_text]['재고'], drink_list[_drink.label_text]['가격'], user.wallet['Card'].get_balance(cash_increase_combo.get()))
                    else:
                        _drink.state_btn['text'] = "●        구매가능"
                        _drink.state_btn['fg'] = "green"
                        _drink.state_btn['state'] = "normal"

            else:
                # 카드 제거
                # TODO 카드 총 사용 내역 기능 추가 예정
                amount_increase_btn['text'] = "카드 투입"
                amount_increase_btn['fg'] = "black"
                user.card_return(cash_increase_combo.get())

                for _drink in self.drink_content:
                    _drink.state_btn['text'] = "○        구매불가"
                    _drink.state_btn['state'] = "disabled"

                machine_amount_label['text'] = f"투입된 금액:\t{machine_amount}원"

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

ua = UserApplication()
ua.window.mainloop()