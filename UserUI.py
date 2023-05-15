from tkinter import *
import customtkinter
import tkinter.messagebox
from PIL import ImageTk
from PIL import Image


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

ctk_window = customtkinter.CTk()
ctk_window.title("자판기")

# 창의 초기 생성위치 설정
ctk_window.config(padx=30, pady=20)
# 창 크기 조절 금지
ctk_window.resizable(False, False)

state_btn = customtkinter.CTkButton(ctk_window, fg_color="transparent", border_width=2, text_color=("green", "green"), text="●          판매중")
label = customtkinter.CTkLabel(ctk_window, text="임시음료", font=customtkinter.CTkFont(size=12, weight="bold"))
price_label = customtkinter.CTkLabel(ctk_window, text="임시가격", font=customtkinter.CTkFont(size=12, weight="bold"))
img = customtkinter.CTkImage(light_image=Image.open(r"images/drink.png"),
                                  dark_image=Image.open(r"images/drink.png"),
                                  size=(64, 64))
image_label = customtkinter.CTkLabel(ctk_window, image=img, text="")
image_label.grid(row=0, column=0)
label.grid(row=1, column=0)
price_label.grid(row=2, column=0, pady=(0, 10))
state_btn.grid(row=3, column=0)

tabview = customtkinter.CTkTabview(ctk_window, width=250)
tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
tabview.add("CTkTabview")
tabview.add("Tab 2")
tabview.add("Tab 3")
tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)




# main_label = customtkinter.CTkLabel(ctk_window, text="  Vending Machine", font=customtkinter.CTkFont(size=20, weight="bold"))
# main_label.grid(row=0, column=2, columnspan=4)
# customtkinter.CTkLabel(ctk_window, text="").grid(row=1, column=0)
#
# id_label = customtkinter.CTkLabel(ctk_window, text="ID:  ", font=customtkinter.CTkFont(size=15))
# pw_label = customtkinter.CTkLabel(ctk_window, text="PW:  ", font=customtkinter.CTkFont(size=15))
# id_label.grid(row=2, column=0, columnspan=2, pady=10)
# pw_label.grid(row=3, column=0, columnspan=2, pady=20)
#
# id_input = customtkinter.CTkEntry(ctk_window, placeholder_text=" ID")
# id_input.grid(row=2, column=2, columnspan=6, ipadx=60)
# # Password 입력시 보이지 않도록 설정
# pw_input = customtkinter.CTkEntry(ctk_window, placeholder_text=" PW", show="*")
# pw_input.grid(row=3, column=2, columnspan=6, ipadx=60)
# customtkinter.CTkLabel(ctk_window, text="").grid(row=4, column=0)
#
#
# login_btn = customtkinter.CTkButton(ctk_window, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="●          판매중")
# login_btn.grid(row=5, column=1, columnspan=3, padx=20)
# reg_btn = customtkinter.CTkButton(ctk_window, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="회원가입")
# reg_btn.grid(row=5, column=4, columnspan=3, padx=20)
# login_btn = Button(text="로그인", width=300, command=login_check, focusthickness=0)
# login_btn['activebackground'] = 'grey'


# # UserRegisterApplication 연결하기
# def register_check():
#     login_window.destroy()
#     subprocess.Popen('python3 UserRegisterApplication.py', shell=True)


# register_btn = Button(text="회원가입", width=300, command=register_check, focusthickness=0)
# register_btn['activebackground'] = 'grey'
# register_btn.grid(row=6, column=0, columnspan=5)
# Label(text="").grid(row=7, column=0)
# # 엔터로 로그인 함수 실행 기능
# login_window.bind("<Return>", login_check)

ctk_window.mainloop()
