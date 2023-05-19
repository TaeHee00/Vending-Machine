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
from controller import ManagerController
from controller import VMController
import Server

import sys, os
import subprocess


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

ctk_window = customtkinter.CTk()
ctk_window.title("Manager Login System")
ctk_window.geometry("+500+200")

# 창의 초기 생성위치 설정
ctk_window.config(padx=30, pady=20)
# 창 크기 조절 금지
ctk_window.resizable(False, False)

main_label = customtkinter.CTkLabel(ctk_window, text="             Manager", font=customtkinter.CTkFont(size=20, weight="bold"))
main_label.grid(row=0, column=2, columnspan=4)
customtkinter.CTkLabel(ctk_window, text="").grid(row=1, column=0)

id_label = customtkinter.CTkLabel(ctk_window, text="ID:  ", font=customtkinter.CTkFont(size=15))
pw_label = customtkinter.CTkLabel(ctk_window, text="PW:  ", font=customtkinter.CTkFont(size=15))
id_label.grid(row=2, column=0, columnspan=2, pady=10)
pw_label.grid(row=3, column=0, columnspan=2, pady=20)

id_input = customtkinter.CTkEntry(ctk_window, placeholder_text=" ID")
id_input.grid(row=2, column=2, columnspan=6, ipadx=60)
# Password 입력시 보이지 않도록 설정
pw_input = customtkinter.CTkEntry(ctk_window, placeholder_text=" PW", show="*")
pw_input.grid(row=3, column=2, columnspan=6, ipadx=60)
customtkinter.CTkLabel(ctk_window, text="").grid(row=4, column=0)

# 로그인 함수
# 엔터로 로그인 함수 실행 시 event인자가 들어오는데 이경우 에러가 발생하기 때문에
# *temp <- 가변인자를 사용하여 처리

def login_check(*temp):
    managerController = ManagerController.ManagerController()
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
        isLogin = False
        if id_input.get() == "manager" and pw_input.get() == "manager":
            showinfo("환영합니다!", f"어서오세요 매니저님!")
            login_window.destroy()
            subprocess.Popen('python3 ManagerApplication.py', shell=True)
            isLogin = True
        if not isLogin:
            # 로그인 실패
            showerror("로그인 오류!", "등록되지 않은 아이디이거나 아이디 또는 비밀번호를 잘못 입력했습니다.")


login_btn = customtkinter.CTkButton(ctk_window, fg_color="transparent", border_width=2,
                                    text_color=("gray10", "#DCE4EE"), text="로그인",
                                    command=login_check)
login_btn.grid(row=5, column=1, columnspan=6, ipadx=60, padx=25)

# 엔터로 로그인 함수 실행 기능
ctk_window.bind("<Return>", login_check)
ctk_window.mainloop()
