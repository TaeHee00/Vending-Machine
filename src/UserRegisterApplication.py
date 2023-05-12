from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkmacosx import Button
import sys
import os

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from dao.UserDao import UserDao
from controller import UserController


class UserRegisterApplication:

    def __init__(self):
        self.userController = UserController.UserController()
        self.window = Tk()
        self.window.title("User Register System")
        # 창의 초기 생성위치 설정
        self.window.geometry("+500+200")
        self.window.config(padx=30, pady=10)
        # 창 크기 조절 금지
        self.window.resizable(False, False)

        self.main_label = Label(text="Vending Machine", font=('Helvetica', 24, "bold"), padding=20)
        self.main_label.grid(row=0, column=0, columnspan=5)

        self.id_label = Label(text="ID")
        self.name_label = Label(text="NAME")
        self.pw_label = Label(text="PASSWORD")
        self.con_pw_label = Label(text="CONFIRM PASSWORD")
        self.name_label.grid(row=2, column=1)
        self.id_label.grid(row=3, column=1)
        self.pw_label.grid(row=4, column=1)
        self.con_pw_label.grid(row=5, column=1)

        self.name_input = Entry()
        self.name_input.grid(row=2 ,column=2, columnspan=2)
        self.id_input = Entry()
        self.id_input.grid(row=3, column=2, columnspan=2)
        # Password 입력시 보이지 않도록 설정
        self.pw_input = Entry(show="*")
        self.pw_input.grid(row=4, column=2, columnspan=2)
        self.con_pw_input = Entry(show="*")
        self.con_pw_input.grid(row=5, column=2, columnspan=2)

        Label(text="").grid(row=6, column=0)

        self.register_btn = Button(text="회원가입", width=300, command=self.register_btn_click, focusthickness=0)
        self.register_btn['activebackground'] = 'grey'
        self.register_btn.grid(row=7, column=0, columnspan=5)
        Label(text="").grid(row=8, column=0)

    def register_btn_click(self):
        if self.name_input.get() == "":
            showerror("입력 오류!", "이름을 입력해주세요!")
        elif self.id_input.get() == "":
            showerror("입력 오류!", "아이디를 입력해주세요!")
        elif self.pw_input.get() == "":
            showerror("입력 오류!", "비밀번호를 입력해주세요!")
        elif self.con_pw_input.get() == "":
            showerror("입력 오류!", "비밀번호 확인을 입력해주세요!")
        elif self.pw_input.get() != self.con_pw_input.get():
            showerror("입력 오류!", "비밀번호와 비밀번호 확인이 일치하지 않습니다!")
        # elif self.id_input.get() == "manager" and self.pw_input.get() == "manager":
        #     # TODO 총 음료 판매 개수 및 수익 재고 경고 목록 띄우기
        #     # TODO 재고 경고 선택 가능하게 만들기
        #     showinfo("환영합니다!", f"어서오세요 {self.name_input.get()}님!")
        #     # 원래 있던 창을 파괴 후 새로운 창 생성
        #     self.window.destroy()
        #     # ua = UserApplication()
        #     # ua.window.mainloop()
        else:
            # TODO 중복처리
            # TODO 회원가입
            userDao = UserDao(self.id_input.get(), self.pw_input.get(), self.name_input.get())
            res = self.userController.userRegister(userDao)
            if res == "성공":
                showinfo("회원가입", "성공적으로 회원가입하셨습니다!")
                self.window.destroy()
            elif res == "중복":
                showerror("에러", "중복된 계정이 있습니다.\n 아이디를 변경해주세요.")

URA = UserRegisterApplication()
URA.window.mainloop()