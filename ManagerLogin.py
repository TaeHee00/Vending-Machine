from tkinter import *
from tkinter.messagebox import *


login_window = Tk()
login_window.title("manager")
# 창의 초기 생성위치 설정
login_window.config(padx=30, pady=20)
login_window.geometry("+500+200")
login_window.resizable(False, False)

main_label = Label(text="Management System", font=('Helvetica', 24, "bold"), pady=10)
main_label.grid(row=0, column=0, columnspan=5)

id_label = Label(text="ID")
pw_label = Label(text="PASSWORD")
id_label.grid(row=2, column=1)
pw_label.grid(row=3, column=1)

id_input = Entry()
id_input.grid(row=2, column=2, columnspan=2)
pw_input = Entry(show="*")
pw_input.grid(row=3, column=2, columnspan=2)

Label(text="").grid(row=4, column=0)


def login_check():
    if id_input.get() == "":
        showerror("입력 오류!", "아이디를 입력해주세요!")
    elif pw_input.get() == "":
        showerror("입력 오류!", "비밀번호를 입력해주세요!")
    elif id_input.get() == "manager" and pw_input.get() == "manager":
        # TODO 총 음료 판매 개수 및 수익 재고 경고 목록 띄우기
        # TODO 재고 경고 선택 가능하게 만들기
        showinfo("환영합니다!", "어서오세요 매니저님!")
        login_window.destroy()
        from test1 import SampleApp
        SampleApp()

    else:
        showerror("로그인 오류!", "일치하는 정보가 없습니다!")


login_btn = Button(text="Login", width=30, command=login_check)
login_btn.grid(row=5, column=0, columnspan=5)
Label(text="").grid(row=6, column=0)
login_window.mainloop()