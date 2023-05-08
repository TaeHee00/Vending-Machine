from tkinter import *
from tkinter.messagebox import *


login_window = Tk()
login_window.title("Management System")
# 창의 초기 생성위치 설정
login_window.geometry("+500+200")
login_window.config(padx=30, pady=20)
# 창 크기 조절 금지
login_window.resizable(False, False)

main_label = Label(text="Management System", font=('Helvetica', 24, "bold"), pady=10)
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
    if id_input.get() == "":
        showerror("입력 오류!", "아이디를 입력해주세요!")
    elif pw_input.get() == "":
        showerror("입력 오류!", "비밀번호를 입력해주세요!")
    elif id_input.get() == "manager" and pw_input.get() == "manager":
        # TODO 총 음료 판매 개수 및 수익 재고 경고 목록 띄우기
        # TODO 재고 경고 선택 가능하게 만들기
        showinfo("환영합니다!", "어서오세요 매니저님!")
        # 원래 있던 창을 파괴 후 새로운 창 생성
        login_window.destroy()
        # 상단에 import할 경우 코드를 읽으면서 먼저 창을 생성해버리는 현상 발생
        # 로그인 성공시 import 하여 객체 생성으로 변경
        from Manager import ManagementMenu
        ManagementMenu.ManagementMenu()
        from Manager import Drink

    else:
        showerror("로그인 오류!", "일치하는 정보가 없습니다!")


login_btn = Button(text="Login", width=30, command=login_check)
login_btn.grid(row=5, column=0, columnspan=5)
Label(text="").grid(row=6, column=0)
# 엔터로 로그인 함수 실행 기능
login_window.bind("<Return>", login_check)

login_window.mainloop()
