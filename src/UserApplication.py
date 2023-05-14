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


# TODO 카드 구매기능 구현
# TODO 구매시 src inventory에 저장하도록 구현
# TODO 구매시 금액 차감후 실시간 정보 변경(카드 정보 수정 및 기타 금액 출력부분 Refrash)

# TODO 화폐 구매기능 구현
# TODO 구매시 잔액 계산 후 나머지돈 Return
# TODO 나머지돈을 화폐 재고에 맞게 Return
# TODO 화폐 재고가 부족할 경우에도 구매 불가능하도록 설정
class UserApplication:

    def __init__(self, user_seq, user_id, user_name):
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
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
        self.window = customtkinter.CTk()
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
        self.img = customtkinter.CTkImage(light_image=Image.open(r"../images/drink.png"),
                               dark_image=Image.open(r"../images/drink.png"),
                               size=(64, 64))
        self.img_cola = customtkinter.CTkImage(light_image=Image.open(r"../images/cola.png"),
                               dark_image=Image.open(r"../images/cola.png"),
                               size=(64, 64))
        self.img_water = ImageTk.PhotoImage(file=r"../images/water.png")
        self.img_cider = ImageTk.PhotoImage(file=r"../images/cider.png")
        self.img_mongo = ImageTk.PhotoImage(file=r"../images/mongo.png")
        self.img_coffee = ImageTk.PhotoImage(file=r"../images/coffee.png")
        self.img_lemon = ImageTk.PhotoImage(file=r"../images/lemon.png")
        self.img_choco = ImageTk.PhotoImage(file=r"../images/choco.png")
        self.img_apple = ImageTk.PhotoImage(file=r"../images/apple.png")
        self.img_energy_drink = ImageTk.PhotoImage(file=r"../images/energy-drink.png")

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
            drinkDto.state_btn['command'] = lambda i=drinkDto.label_text, j=drinkDto.drink_price, k=self.user_seq: [self.drink_buy_pay(i, j, k)]
            self.drink_content.append(drinkDto)

            if drinkDto.label_text == '물':
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_water)
            elif '콜라' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_cola)
            elif '사이다' in drinkDto.label_text or '트레비' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_cider)
            elif '망고' in drinkDto.label_text or '립톤' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_mongo)
            elif '핫식스' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_energy_drink)
            elif '레몬' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_lemon)
            elif '가나' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_choco)
            elif '사과' in drinkDto.label_text or '게토레이' in drinkDto.label_text or '마운틴듀오' in drinkDto.label_text or '코코 포도' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_apple)
            elif '콘트라베이스' in drinkDto.label_text or '레쓰비' in drinkDto.label_text:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2,
                                                                 image=self.img_coffee)
            else:
                self.drink_content[self.idx].canvas.create_image(self.img_size / 2, self.img_size / 2, image=self.img)

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
        # 유저 지갑 데이터베이스 연동
        userController = UserController.UserController()

        self.user_card = userController.userCardList(self.user_seq)
        self.user_cash = userController.userCashList(self.user_seq)
        # 자판기 실행시 manager_wallte['Temp_Card'] 내용 초기화

        # 자판기에 투입된 금액 표시
        self.machine_amount_label = Label(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원", font="Helvetica 16 bold")
        # 가로로 진열할 음료의 개수가 2보다 적어도 오류가 발생하지 않도록 절대값을 사용
        self.machine_amount_label.grid(row=99, column=abs(self.row_limit - 2), columnspan=3)

        Label(text=" ").grid(row=100, column=self.column_cnt)
        self.cash_list = list()
        for cash in self.user_cash:
            self.cash_list.append(f"{cash.getCashName()}원: {cash.getCashAmount()}개")
        self.user_cash_list = list(self.cash_list)

        self.card_list = list()
        for card in self.user_card:
            self.card_list.append(f"{card.getCardName()}: {card.getCardAmount()}원")
        self.user_card_list = list(self.card_list)

        # 현금반환 기능 추가
        # 현금 반환시 구매버튼 모두 비활성화
        self.amount_return_btn = Button(text="현금 반환", focusthickness=0, activebackground='gray', width=160)
        self.amount_return_btn.grid(row=102, column=abs(self.row_limit - 3))

        # 현금 결제를 위한 Drop-down 옵션
        # 자판기와 동일한 동작을 위해 화폐는 하나씩 투입하도록 설정
        # 화폐 투입 전 구매 버튼 비활성화
        self.amount_increase_combo = Combobox(self.window, width=15, state='readonly')
        self.amount_increase_combo['value'] = self.user_cash_list
        self.amount_increase_combo.current(0)
        self.amount_increase_combo.grid(row=101, column=abs(self.row_limit - 2))
        self.amount_increase_btn_cash = Button(text="현금 투입", focusthickness=0, activebackground='gray', width=160)
        self.amount_increase_btn_cash.grid(row=102, column=abs(self.row_limit - 2))

        # 카드 결제를 위한 Drop-down 옵션
        # 카드를 투입 후 반환 전까지 카드의 잔액을 사용하여 결제
        # 카드 투입 전 구매 버튼 비활성화
        self.cash_increase_combo = Combobox(self.window, width=15, state='readonly')
        self.cash_increase_combo['value'] = self.user_card_list
        self.cash_increase_combo.current(0)
        self.cash_increase_combo.grid(row=101, column=abs(self.row_limit - 1))
        self.amount_increase_btn_card = Button(text="카드 투입", focusthickness=0, activebackground='gray', width=160)
        self.amount_increase_btn_card.grid(row=102, column=abs(self.row_limit - 1))


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
            self.machine_amount_label["text"] = f"카드 잔액:\t{self.user_card[0].getCardAmount()}원"
            self.card_list[0] = f"{self.user_card[0].getCardName()}: {self.user_card[0].getCardAmount()}원"
            self.cash_increase_combo.config(values=self.card_list)
            self.cash_increase_combo.current(0)
            # VM drink 재고 감소
            drink_seq = self.vmController.drinkStockDecrease(drink_name)
            # User Bag에 추가
            self.userController.bagDrinkIncrease(self.user_seq, drink_seq)
            # Manager_Bank에 잔액 추가
            self.vmController.cashIncrease(drink_price)
            # 구매 메세지 출력
            showinfo("결제 정보", f"음료명: {drink_name}\n가격: {drink_price}\n1개를 구매하셨습니다.\n\n{self.user_card[0].getCardName()} 잔액\n {int(self.user_card[0].getCardAmount()) + drink_price}원  ->  {self.user_card[0].getCardAmount()}원")
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
            vm_cash_stock = self.vmController.vmCashStock() # manager cash list 가져오기

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
            self.machine_amount_label.config(text=f"투입된 금액:\t{self.temp_cash_cnt['total']}원")
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
            showinfo("결제 정보", f"음료명: {drink_name}\n가격: {drink_price}\n1개를 구매하셨습니다.\n\n투입된 금액 잔액\n {int(self.temp_cash_cnt['total']) + drink_price}원  ->  {int(self.temp_cash_cnt['total'])}원")





login_window = Tk()
login_window.title("User Login System")
# 창의 초기 생성위치 설정
login_window.geometry("+500+200")
login_window.config(padx=30, pady=20)
# 창 크기 조절 금지
login_window.resizable(False, False)

main_label = Label(text="Vending Machine", font=('Helvetica', 24, "bold"), padding=20)
main_label.grid(row=0, column=0, columnspan=5)

id_label = Label(text="ID")
pw_label = Label(text="PASSWORD")
id_label.grid(row=2, column=1)
pw_label.grid(row=3, column=1)

id_input = Entry()
id_input.grid(row=2, column=2, columnspan=2)
# Password 입력시 보이지 않도록 설정
pw_input = Entry(show="*")
pw_input.grid(row=3, column=2, columnspan=2)

Label(text="").grid(row=4, column=0)


# 로그인 함수
# 엔터로 로그인 함수 실행 시 event인자가 들어오는데 이경우 에러가 발생하기 때문에
# *temp <- 가변인자를 사용하여 처리
def login_check(*temp):
    userController = UserController.UserController()
    user_list = userController.userList()

    if id_input.get() == "":
        showerror("입력 오류!", "아이디를 입력해주세요!")
    elif pw_input.get() == "":
        showerror("입력 오류!", "비밀번호를 입력해주세요!")
    # TODO 데이터 가져와서 계정 확인 후 로그인
    # TODO 총 음료 판매 개수 및 수익 재고 경고 목록 띄우기
    # TODO 재고 경고 선택 가능하게 만들기
    else:
        # TODO 로그인 성공 & 실패
        user_seq = ""
        user_id = ""
        user_name = ""
        isLogin = False
        for user in user_list:
            # 로그인 성공
            if id_input.get() == user[1] and pw_input.get() == user[2]:
                user_seq = user[0]
                user_id = user[1]
                user_name = user[3]
                # print(user_seq, user_id, user_name)
                showinfo("환영합니다!", f"어서오세요 {user_name}님!")
                # 원래 있던 창을 파괴 후 새로운 창 생성
                login_window.destroy()
                ua = UserApplication(user_seq, user_id, user_name)
                server = Server.Server(ua)
                ua.window.mainloop()
                isLogin = True
                break
        if not isLogin:
            # 로그인 실패
            showerror("로그인 오류!", "등록되지 않은 아이디이거나 아이디 또는 비밀번호를 잘못 입력했습니다.")


login_btn = Button(text="로그인", width=300, command=login_check, focusthickness=0)
login_btn['activebackground'] = 'grey'


# UserRegisterApplication 연결하기
def register_check():
    login_window.destroy()
    subprocess.Popen('python3 UserRegisterApplication.py', shell=True)


register_btn = Button(text="회원가입", width=300, command=register_check, focusthickness=0)
register_btn['activebackground'] = 'grey'
login_btn.grid(row=5, column=0, columnspan=5)
register_btn.grid(row=6, column=0, columnspan=5)
Label(text="").grid(row=7, column=0)
# 엔터로 로그인 함수 실행 기능
login_window.bind("<Return>", login_check)

login_window.mainloop()
