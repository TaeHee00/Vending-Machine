from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkmacosx import Button
import customtkinter
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from PIL import Image
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json
from controller import DrinkController
from controller import UserController
from controller import VMController
import Server

import sys, os
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dto import VM_DrinkDto


# TODO 화폐 재고가 부족할 경우에도 구매 불가능하도록 설정
class UserApplication:

    def __init__(self, user_seq, user_id, user_name):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        self.window = customtkinter.CTk()
        with open("/Users/mac/Vending-Machine/src/flag.json", "r") as file:
            flag_data = json.load(file)

        with open("/Users/mac/Vending-Machine/src/flag.json", "w") as file:
            flag_data['flag'] = ''
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)

        self.user_seq = user_seq
        self.user_id = user_id
        self.user_name = user_name

        self.machine_amount = 0
        self.temp_cash_cnt = {
            '5000': 0,
            '1000': 0,
            '500': 0,
            '100': 0,
            'total': 0
        }

        self.drinkController = DrinkController.DrinkController()
        self.userController = UserController.UserController()
        self.vmController = VMController.VMController()
        # self.server = Server.Server()
        self.window.title("자판기")
        # 창의 초기 생성위치 설정
        self.window.configure(padx=30, pady=20)
        self.window.geometry("+200+0")
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

        # drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
        vm_drink_list = self.drinkController.vmDrinkList()
        drink_list = self.drinkController.drinkList()

        for drink in vm_drink_list:
            drinkDto = VM_DrinkDto.VM_DrinkDto(
                window=self.window,
                label=drink_list[drink.getDrinkSeq() - 1].getDrinkName(),
                stock=drink.getAmount(),
                state="판매불가",
                price=drink.getDrinkUserPrice(),
                content_id=drink.getDrinkSeq()
            )
            drinkDto.state_btn.configure(
                command= lambda i=drinkDto.label_text,
                                j=drinkDto.drink_price,
                                k=self.user_seq: [self.drink_buy_pay(i, j, k)]
            )
            self.drink_content.append(drinkDto)

            # 객체 생성
            self.drink_content[self.idx].canvas.grid(row=self.row_cnt, column=self.column_cnt)
            # self.drink_content[self.idx].canvas.update()
            self.drink_content[self.idx].label.grid(row=self.row_cnt + 1, column=self.column_cnt)
            self.drink_content[self.idx].price_label.grid(row=self.row_cnt + 2, column=self.column_cnt)
            drink_name = self.drink_content[self.idx].label_text
            drink_price = self.drink_content[self.idx].drink_price
            # self.drink_content[self.idx].state_btn.config(
            #     command=lambda: drink_buy_event(
            #         drink_name,
            #         drink_price
            #     )
            # )
            self.drink_content[self.idx].state_btn.grid(row=self.row_cnt + 3, column=self.column_cnt, padx=15)

            self.column_cnt += 1
            customtkinter.CTkLabel(self.window, text=" ").grid(row=self.row_cnt + 4, column=self.column_cnt)
            customtkinter.CTkLabel(self.window, text=" ").grid(row=self.row_cnt + 5, column=self.column_cnt)
            # customtkinter.CTkLabel(self.window, text=" ").grid(row=self.row_cnt + 6, column=self.column_cnt)
            if self.column_cnt % self.row_limit == 0:
                # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
                self.column_cnt = 0
                self.row_cnt += 5
            self.idx += 1

        # 자판기 사용 유저의 지갑
        # cash: 현금 저장용
        # card: 카드 저장용
        # 유저 지갑 데이터베이스 연동
        userController = UserController.UserController()

        self.user_card = userController.userCardList(self.user_seq)
        self.user_cash = userController.userCashList(self.user_seq)
        # 자판기 실행시 manager_wallte['Temp_Card'] 내용 초기화

        # 자판기에 투입된 금액 표시
        self.machine_amount_label = customtkinter.CTkLabel(self.window, text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원",
                                                           font=customtkinter.CTkFont(size=16, weight="bold"))
        # 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
        self.machine_amount_label.grid(row=99, column=abs(self.row_limit - 2))

        customtkinter.CTkLabel(self.window, text=" ").grid(row=100, column=self.column_cnt)
        self.cash_list = list()
        for cash in self.user_cash:
            if cash.getCashName() == "5000":
                continue
            self.cash_list.append(f"{cash.getCashName()}원: {cash.getCashAmount()}개")
        self.user_cash_list = self.cash_list


        self.card_list = list()
        for card in self.user_card:
            self.card_list.append(f"{card.getCardName()}: {card.getCardAmount()}원")

        self.btn_size = 11
        # 현금반환 기능 추가
        # 현금 반환시 구매버튼 모두 비활성화
        self.amount_return_btn = customtkinter.CTkButton(
            self.window,
            fg_color="transparent",
            text="현금 반환",
            border_width=2,
            command=self.cash_return_event
        )
        self.amount_return_btn.grid(row=102, column=abs(self.row_limit - 3),
                                    ipadx=self.btn_size)

        # 현금 결제를 위한 Drop-down 옵션
        # 자판기와 동일한 동작을 위해 화폐는 하나씩 투입하도록 설정
        # 화폐 투입 전 구매 버튼 비활성화
        self.amount_increase_combo = customtkinter.CTkComboBox(
            self.window,
            state='readonly',
            values=self.user_cash_list,
            width=162
        )
        self.amount_increase_combo.grid(row=101, column=abs(self.row_limit - 2), pady=(0, 3))
        self.amount_increase_combo.set(self.user_cash_list[0])
        self.amount_increase_btn_cash = customtkinter.CTkButton(
            self.window,
            fg_color="transparent",
            text="현금 투입",
            border_width=2,
            command=self.cash_injection_event
        )
        self.amount_increase_btn_cash.grid(row=102, column=abs(self.row_limit - 2),
                                           ipadx=self.btn_size)
        # 카드 결제를 위한 Drop-down 옵션
        # 카드를 투입 후 반환 전까지 카드의 잔액을 사용하여 결제
        # 카드 투입 전 구매 버튼 비활성화
        self.cash_increase_combo = customtkinter.CTkComboBox(
            self.window,
            state='readonly',
            values=self.user_cash_list,
            width=162
        )
        self.cash_increase_combo.grid(row=101, column=abs(self.row_limit - 1), pady=(0, 3))
        self.cash_increase_combo.set(self.user_cash_list[0])
        self.amount_increase_btn_card = customtkinter.CTkButton(
            self.window,
            text="카드 투입",
            fg_color="transparent",
            border_width=2,
            command=self.card_injection_event
        )
        self.amount_increase_btn_card.grid(row=102, column=abs(self.row_limit - 1),
                                           ipadx=self.btn_size)

    def drink_buy_pay(self, drink_name, drink_price, user_seq):
        # cash인지 card인지 확인
        with open("flag.json", "r") as file:
            flag = json.load(file)

        # Card일 경우
        if flag['flag'] == "card":
            # Card 잔액 감소
            self.userController.drinkBuyCard(drink_price, self.user_card[0].getCardSeq())
            # Interface의 Card 잔액 수정
            self.user_card[0].setCardAmount(self.user_card[0].getCardAmount() - drink_price)
            self.machine_amount_label.configure(text=f"카드 잔액:\t{self.user_card[0].getCardAmount()}원")
            self.card_list[0] = f"{self.user_card[0].getCardName()}: {self.user_card[0].getCardAmount()}원"
            self.cash_increase_combo.configure(values=self.card_list)
            self.cash_increase_combo.set(self.card_list[0])
            # VM drink 재고 감소
            drink_seq = self.vmController.drinkStockDecrease(drink_name)
            # User Bag에 추가
            self.userController.bagDrinkIncrease(self.user_seq, drink_seq)
            # Manager_Bank에 잔액 추가
            self.vmController.cashIncrease(drink_price)
            # 구매 메세지 출력
            showinfo("결제 정보",
                     f"음료명: {drink_name}\n"
                     f"가격: {drink_price}\n"
                     f"1개를 구매하셨습니다.\n\n"
                     f"{self.user_card[0].getCardName()} 잔액\n "
                     f"{int(self.user_card[0].getCardAmount()) + drink_price}원  ->  {self.user_card[0].getCardAmount()}원")
        elif flag['flag'] == "cash":
            # Cash일 경우
            # 현금은 빠진 상태
            # UserApplication -> self.temp_cash_cnt['total']을 음료수 가격 만큼 감소
            self.temp_cash_cnt['total'] -= drink_price
            # UserApplication -> self.temp_cash_cnt 화폐 개수 수정
            self.temp_cash_cnt['5000'] = 0
            self.temp_cash_cnt['1000'] = 0
            self.temp_cash_cnt['500'] = 0
            self.temp_cash_cnt['100'] = 0
            # 화폐 개수 수정) 전부 개수 0으로 변경 후 greedy algorithm을 사용하여 가장 반환에 가장 적합한 화폐 선정
            # VM_Machine에 화폐가 부족할 경우 down-casting 하여 반환
            # 가져온 다음 5000원 부터 반대로 내려오면 개수 선정 후 self.temp_cash_cnt에 저장
            vm_cash_stock = self.vmController.vmCashStock()  # manager cash list 가져오기

            sd = self.temp_cash_cnt['total']
            # 반환할 수 있는 화폐가 1개 이상 있는 경우
            if vm_cash_stock['5000'] > 0:

                if sd > 0:
                    rt = int(sd / 5000)
                    # 반환 할 수 있는 지폐가 충분한 경우
                    if vm_cash_stock['5000'] >= rt:
                        # 유저 cash목록에 저장
                        self.temp_cash_cnt['5000'] = rt
                        sd = int(sd % 5000)
                    # 반환 할 수 있는 지폐가 부족한 경우
                    else:
                        # 재고의 cash잔고의 모든 재고를 이동
                        self.temp_cash_cnt['5000'] = vm_cash_stock['5000']
                        sd -= int(vm_cash_stock['5000'] * 5000)

                if sd > 0:
                    rt = int(sd / 1000)
                    if vm_cash_stock['1000'] >= rt and sd > 0:
                        # 유저 cash목록에 저장
                        self.temp_cash_cnt['1000'] = rt
                        sd = int(sd % 1000)
                    # 반환 할 수 있는 지폐가 부족한 경우
                    else:
                        # 재고의 cash잔고의 모든 재고를 이동
                        self.temp_cash_cnt['1000'] = vm_cash_stock['1000']
                        sd -= int(vm_cash_stock['1000'] * 1000)

                if sd > 0:
                    rt = int(sd / 500)
                    if vm_cash_stock['500'] >= rt and sd > 0:
                        # 유저 cash목록에 저장
                        self.temp_cash_cnt['500'] = rt
                        sd = int(sd % 500)
                    # 반환 할 수 있는 지폐가 부족한 경우
                    else:
                        # 재고의 cash잔고의 모든 재고를 이동
                        self.temp_cash_cnt['500'] = vm_cash_stock['500']
                        sd -= int(vm_cash_stock['500'] * 500)

                if sd > 0:
                    rt = int(sd / 100)
                    if vm_cash_stock['100'] >= rt and sd > 0:
                        # 유저 cash목록에 저장
                        self.temp_cash_cnt['100'] = rt
                        sd = int(sd % 100)
                    # 반환 할 수 있는 지폐가 부족한 경우
                    else:
                        # 재고의 cash잔고의 모든 재고를 이동
                        self.temp_cash_cnt['100'] = vm_cash_stock['100']
                        sd -= int(vm_cash_stock['100'] * 100)

                # VM_Machine에 화폐가 부족할 경우 알람 or Print문으로 경고
                if sd > 0:
                    # ERROR 현금 반환 재고 부족
                    print("[ERROR]\t현금 잔액이 부족하여 반환에 실패하였습니다.")
                    print(f"[ERROR]\t반환 실패 금액: {sd}원")

            # TODO 각 화폐가 N개 이하(default = 20)로 떨어지면 경고

            # TODO Interface의 Cash 투입 금액 수정
            # 투입 금액을 self.temp_cash_cnt['total']로 수정
            self.machine_amount_label.configure(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원")
            # drop-down value 전부 수정
            # self.user_cash_list[0] = f"5000원: {self.temp_cash_cnt['5000']}개"
            # self.user_cash_list[1] = f"1000원: {self.temp_cash_cnt['1000']}개"
            # self.user_cash_list[2] = f"500원: {self.temp_cash_cnt['500']}개"
            # self.user_cash_list[3] = f"100원: {self.temp_cash_cnt['100']}개"
            # self.amount_increase_combo.config(values=self.user_cash_list)
            # VM drink 재고 감소
            drink_seq = self.vmController.drinkStockDecrease(drink_name)
            # User Bag에 추가
            self.userController.bagDrinkIncrease(self.user_seq, drink_seq)
            # 구매 메세지 출력
            showinfo("결제 정보",
                     f"음료명: {drink_name}\n가격: {drink_price}\n"
                     f"1개를 구매하셨습니다.\n\n투입된 금액 잔액\n "
                     f"{int(self.temp_cash_cnt['total']) + drink_price}원  ->  {int(self.temp_cash_cnt['total'])}원")

    def cash_injection_event(self):
        # 결제 할 수단을 cash로 변경
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = 'cash'
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # DB 연결 후 실시간 데이터 받아오기
        select_cash = self.amount_increase_combo.get().replace("원:", "").replace("개", "").split()
        cash_name = select_cash[0]
        # 선택한 지폐(화폐)가 1개 이상인지 확인
        if int(select_cash[1]) > 0:
            # User Cash decrease
            self.userController.userCashDecrease(self.user_seq, select_cash[0])
            # User Interface Cash decrease & Update
            idx = 0
            for user_cash in self.user_cash_list:
                if cash_name + "원" in user_cash:
                    self.user_cash_list[idx] = f"{cash_name}원: {int(select_cash[1]) - 1}개"
                    break
                idx += 1
            self.amount_increase_combo.configure(values=self.user_cash_list)
            if "1000원" in self.amount_increase_combo.get():
                self.amount_increase_combo.set(self.user_cash_list[0])
                self.machine_amount += 1000
                self.temp_cash_cnt['total'] += 1000
            elif "500원" in self.amount_increase_combo.get():
                self.amount_increase_combo.set(self.user_cash_list[1])
                self.machine_amount += 500
                self.temp_cash_cnt['total'] += 500
            elif "100원" in self.amount_increase_combo.get():
                self.amount_increase_combo.set(self.user_cash_list[2])
                self.machine_amount += 100
                self.temp_cash_cnt['total'] += 100

            # temp_cash_cnt <- Cash Increase
            self.temp_cash_cnt[cash_name] += 1

            # VM Interface Cash Increase & Update
            self.machine_amount_label.configure(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원",
                                                      font=customtkinter.CTkFont(size=16, weight="bold"))
            # Machine Cash Amount Increase
            self.vmController.managerCashInjection(cash_name)
            # 구매가능 음료 체크
            # 구매가능 음료 상태 변경
            for _drink in self.drink_content:
                # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
                if _drink.stock <= 0 or _drink.drink_price > self.temp_cash_cnt['total']:
                    _drink.state_btn.configure(
                        text="○        구매불가",
                        text_color=("red", "red"),
                        text_color_disabled=("red", "red"),
                        state='disabled'
                   )
                else:
                    _drink.state_btn.configure(
                        text="●        구매가능",
                        text_color=("green", "green"),
                        text_color_disabled=("green", "green"),
                        state="normal"
                    )


    # 카드 삽입시 잔액에 따라 구매 가능한 음료만 판매 상태 변경
    # 카드 삽입,제거시 투입된 금액 Label 변경
    # TODO 구매시 카드 잔액 실시간 업데이트
    # TODO 구매시 user_bag에 음료명: 개수 추가
    # TODO Manager 통계에서 판매 수익 및 판매 음료 추가
    def card_injection_event(self):
        # 결제 할 수단을 card로 변경
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = 'card'
            # TODO card_seq 가져오기
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # 카드 삽입
        if self.amount_increase_btn_card.cget("text") == "카드 투입":
            self.amount_increase_btn_card.configure(
                text=f"{self.cash_increase_combo.get().replace(':', '').split()[0]} 투입됨",
                text_color = ("green", "green"),
                text_color_disabled = ("green", "green")
            )

            # TODO 카드잔액 코드 수정
            self.machine_amount_label.configure(text=f"카드 잔액:\t{self.user_card[0].getCardAmount()}원")

            for _drink in self.drink_content:
                # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
                if _drink.stock <= 0 or _drink.drink_price > int(self.user_card[0].getCardAmount()):
                    _drink.state_btn.configure(
                        text="○        구매불가",
                        text_color=("red", "red"),
                        text_color_disabled=("red", "red"),
                        state='disabled'
                    )
                else:
                    _drink.state_btn.configure(
                        text="●        구매가능",
                        text_color=("green", "green"),
                        text_color_disabled=("green", "green"),
                        state="normal"
                    )

        else:
            # 카드 제거
            # 결제 할 수단을 cash로 변경
            with open("flag.json", "r") as file:
                flag_data = json.load(file)

            with open("flag.json", "w") as file:
                flag_data['flag'] = ''
                flag_data['card_seq'] = ''
                json.dump(flag_data, file, indent=4)
            # TODO 카드 총 사용 내역 기능 추가 예정
            self.amount_increase_btn_card.configure(
                text="카드 투입",
                text_color=("black", "white"),
                text_color_disabled=("black", "white"),
                state="normal"
            )

            for _drink in self.drink_content:
                _drink.state_btn.configure(
                    text="○        구매불가",
                    text_color=("red", "red"),
                    text_color_disabled=("red", "red"),
                    state='disabled'
                )

            self.machine_amount_label.configure(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원")


    def cash_return_event(self):
        # 결제 flag 초기화
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = ''
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # 투입금액이 있는지 확인
        if self.machine_amount <= 0:
            return

        # VMController에 현금 반환 요청
        self.vmController.cashReturn(self.temp_cash_cnt)
        # 반환된 Cash를 UserController에 Cash Injection 요청
        self.userController.cashReturn(self.user_seq, self.temp_cash_cnt)
        # cash ComboBox 객체 수정
        self.select_cash = self.amount_increase_combo.get().replace("원:", "").replace("개", "").split()
        select_cash_name = self.select_cash[0]
        idx = 0
        for _user_cash in self.user_cash_list:
            combo_cash_data = _user_cash.replace("원:", "").replace("개", "").split()
            combo_cash_name = combo_cash_data[0]
            self.user_cash_list[idx] = f"{combo_cash_name}원: {int(combo_cash_data[1]) + int(self.temp_cash_cnt[combo_cash_name])}개"
            idx += 1

        # ComboBox Update
        self.amount_increase_combo.configure(values=self.user_cash_list)
        if "1000" == select_cash_name:
            self.amount_increase_combo.set(self.user_cash_list[0])
        elif "500" == select_cash_name:
            self.amount_increase_combo.set(self.user_cash_list[1])
        elif "100" == select_cash_name:
            self.amount_increase_combo.set(self.user_cash_list[2])

        showinfo("반환 정보",
                 f"총 반환 금액: {self.temp_cash_cnt['total']}원\n\n"
                 f"1000원\t{self.temp_cash_cnt['1000']}개\n"
                 f"500원\t{self.temp_cash_cnt['500']}개\n"
                 f"100원\t{self.temp_cash_cnt['100']}개")

        # self.temp_cash_cnt 초기화
        for _cash in self.temp_cash_cnt:
            self.temp_cash_cnt[_cash] = 0
        self.temp_cash_cnt['total'] = 0
        # 투입 금액 label 초기화
        self.machine_amount_label.configure(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원")
        # 음료 구매 버튼 수정
        for _drink in self.drink_content:
            # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
            _drink.state_btn.configure(
                text="○        구매불가",
                text_color=("red", "red"),
                text_color_disabled=("red", "red"),
                state='disabled'
            )


with open("/Users/mac/Vending-Machine/src/login_data.json", "r") as file:
    login_data = json.load(file)

ua = UserApplication(login_data['user_seq'], login_data['user_id'], login_data['user_name'])
ua.window.mainloop()