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
import Server

from controller import DrinkController
from controller import UserController
from controller import ManagerController
from controller import VMController

import sys, os
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dto import Manager_DrinkDto


# TODO 화폐 재고가 부족할 경우에도 구매 불가능하도록 설정
class ManagerApplication:

    def __init__(self):
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("dark-blue")
        self.window = customtkinter.CTk()

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
        self.managerController = ManagerController.ManagerController()
        self.vmController = VMController.VMController()
        # self.server = Server.Server()
        self.window.title("자판기 관리자")
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
            drinkDto = Manager_DrinkDto.Manager_DrinkDto(
                window=self.window,
                label=drink_list[drink.getDrinkSeq() - 1].getDrinkName(),
                stock=drink.getAmount(),
                state="재고",
                price=int(drink.getDrinkUserPrice()/2),
                content_id=drink.getDrinkSeq()
            )
            self.drink_content.append(drinkDto)

            # state Label에 재고 출력 (재고 없을 경우에 빨간색 출력)
            self.drink_content[self.idx].state_btn.configure(text=f"{self.drink_content[self.idx].stock}개", text_color=("green", "green"), text_color_disabled=("green", "green"))
            self.drink_content[self.idx].state_btn.configure(command=
                         lambda x=self.idx, y=drink.getDrinkSeq(): [self.drink_content[x].open_input_dialog_event(x, y), self.stock_update()])
            # 객체 생성
            self.drink_content[self.idx].canvas.grid(row=self.row_cnt, column=self.column_cnt)
            # self.drink_content[self.idx].canvas.update()
            self.drink_content[self.idx].label.grid(row=self.row_cnt + 1, column=self.column_cnt)
            self.drink_content[self.idx].price_label.grid(row=self.row_cnt + 2, column=self.column_cnt)
            drink_name = self.drink_content[self.idx].label_text
            drink_price = self.drink_content[self.idx].drink_price
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


        self.stock_label = customtkinter.CTkLabel(
            self.window,
            text=f"현재 재고",
            font=customtkinter.CTkFont(size=25, weight="bold")
        ).grid(row=self.row_cnt + 6, column=0, columnspan=1, pady=(0, 20))

        self.price_1000 = customtkinter.CTkLabel(
            self.window,
            text=f"1000원",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        self.price_1000.grid(row=self.row_cnt + 7, column=0)

        self.price_1000_stock = customtkinter.CTkLabel(
            self.window,
            # TODO 일정 개수 이하일 시 빨간색, 이상일시 초록색
            text=f"-개",
            font=customtkinter.CTkFont(size=15)
        )
        self.price_1000_stock.grid(row=self.row_cnt + 8, column=0)
        # self.price_1000_btn = customtkinter.CTkButton(self.window, fg_color="transparent", border_width=2,
        #                                               text_color=("green", "green")).grid(row=self.row_cnt + 8, column=0)

        self.price_500 = customtkinter.CTkLabel(
            self.window,
            text=f"500원",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        self.price_500.grid(row=self.row_cnt + 7, column=1)

        self.price_500_stock = customtkinter.CTkLabel(
            self.window,
            text=f"-개",
            font=customtkinter.CTkFont(size=15)
        )
        self.price_500_stock.grid(row=self.row_cnt + 8, column=1)
        # self.price_500_btn = customtkinter.CTkButton(self.window, fg_color="transparent", border_width=2,
        #                                               text_color=("green", "green")).grid(row=self.row_cnt + 8, column=1)

        self.price_100 = customtkinter.CTkLabel(
            self.window,
            text=f"100원",
            font=customtkinter.CTkFont(size=18, weight="bold")
        )
        self.price_100.grid(row=self.row_cnt + 7, column=2)
        self.price_100_stock = customtkinter.CTkLabel(
            self.window,
            text=f"-개",
            font=customtkinter.CTkFont(size=15)
        )
        self.price_100_stock.grid(row=self.row_cnt + 8, column=2)
        # self.price_100_btn = customtkinter.CTkButton(self.window, fg_color="transparent", border_width=2,
        #                                               text_color=("green", "green")).grid(row=self.row_cnt + 8, column=2)

        # self.card_label = customtkinter.CTkLabel(
        #     self.window,
        #     text=f"관리자 통장",
        #     font=customtkinter.CTkFont(size=18, weight="bold")
        # )
        # self.card_label.grid(row=self.row_cnt + 7, column=3)

        # self.card_amount = customtkinter.CTkLabel(
        #     self.window,
        #     text=f"-원",
        #     font=customtkinter.CTkFont(size=15)
        # )
        # self.card_amount.grid(row=self.row_cnt + 8, column=3)

        self.cash_1000_buy = customtkinter.CTkButton(
            self.window,
            fg_color="transparent",
            text="1000원 재고 추가",
            border_width=2,
            command=self.cash_1000_buy
        )

        self.cash_1000_buy.grid(row=self.row_cnt + 7, column=3)

        self.cash_500_buy = customtkinter.CTkButton(
            self.window,
            fg_color="transparent",
            text="500원 재고 추가",
            border_width=2,
            command=self.cash_500_buy
        )
        self.cash_500_buy.grid(row=self.row_cnt + 7, column=4)

        self.cash_100_buy = customtkinter.CTkButton(
            self.window,
            fg_color="transparent",
            text="100원 재고 추가",
            border_width=2,
            command=self.cash_100_buy
        )
        self.cash_100_buy.grid(row=self.row_cnt + 7, column=5)


        self.stock_update()

    def cash_1000_buy(self):
        card_data = self.managerController.findManagerBank()
        if int(card_data) >= 1000:
            # 통장에서 금액 감소
            self.managerController.decreaseManagerBank(1000)
            # 1000원 금액추가
            self.managerController.increaseCash1000()
            # Label Update
            self.stock_update()
            print(f"화폐명:\t1000원 재고 추가 성공")
        else:
            print(f"[경고]\t화폐명:\t1000원 재고 추가 실패\n\t잔액 부족")
        print(f"통잔 잔고: {int(card_data) + 500}원    ->    {int(card_data)}원")

    def cash_500_buy(self):
        card_data = self.managerController.findManagerBank()
        if int(card_data) >= 500:
            # 통장에서 금액 감소
            self.managerController.decreaseManagerBank(500)
            # 500원 금액추가
            self.managerController.increaseCash500()
            # Label Update
            self.stock_update()
            print(f"화폐명:\t500원 재고 추가 성공")
        else:
            print(f"[경고]\t화폐명:\t500원 재고 추가 실패\n\t잔액 부족")
        print(f"통잔 잔고: {int(card_data) + 500}원    ->    {int(card_data)}원")

    def cash_100_buy(self):
        card_data = self.managerController.findManagerBank()
        if int(card_data) >= 100:
            # 통장에서 금액 감소
            self.managerController.decreaseManagerBank(100)
            # 100원 금액추가
            self.managerController.increaseCash100()
            # Label Update
            self.stock_update()
            card_data = self.managerController.findManagerBank()
            print(f"화폐명:\t100원 재고 추가 성공")
        else:
            print(f"[경고]\t화폐명:\t100원 재고 추가 실패\n\t잔액 부족")
        print(f"통잔 잔고: {int(card_data) + 100}원    ->    {int(card_data)}원")


    def stock_update(self):

        cash_data = self.managerController.findCash()

        if cash_data[0][2] >= 20:
            self.price_1000_stock.configure(text=f"{cash_data[0][2]}개", text_color=("green", "green"))
        else:
            self.price_1000_stock.configure(text=f"[경고] 현금 재고를 추가하십시오.\n{cash_data[0][2]}개", text_color=("red", "red"))

        if cash_data[1][2] >= 20:
            self.price_500_stock.configure(text=f"{cash_data[1][2]}개", text_color=("green", "green"))
        else:
            self.price_500_stock.configure(text=f"[경고] 현금 재고를 추가하십시오.\n{cash_data[1][2]}개", text_color=("red", "red"))

        if cash_data[2][2] >= 20:
            self.price_100_stock.configure(text=f"{cash_data[2][2]}개", text_color=("green", "green"))
        else:
            self.price_100_stock.configure(text=f"[경고] 현금 재고를 추가하십시오.\n{cash_data[2][2]}개", text_color=("red", "red"))

        # card_data = self.managerController.findManagerBank()


with open("/Users/mac/Vending-Machine/src/login_data.json", "r") as file:
    login_data = json.load(file)

ma = ManagerApplication()
ma.window.mainloop()