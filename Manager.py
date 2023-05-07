from tkinter import *
from tkinter import messagebox

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0)


class LoginPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        main_label = Label(text="Management System", font=('Helvetica', 24, "bold"), pady=10)
        main_label.grid(row=0, column=0, columnspan=5)

        id_label = Label(text="ID")
        pw_label = Label(text="PASSWORD")
        id_label.grid(row=2, column=1)
        pw_label.grid(row=3, column=1)

        self.id_input = Entry()
        self.id_input.grid(row=2, column=2, columnspan=2)
        self.pw_input = Entry()
        self.pw_input.grid(row=3, column=2, columnspan=2)

        Label(text="").grid(row=4, column=0)

        self.login_btn = Button(text="Login", width=30)
        self.login_btn.grid(row=5, column=0, columnspan=5)
        Label(text="").grid(row=6, column=0)

    def login_check(self):
        if self.id_input.get() == "":
            messagebox.showerror("입력 오류!", "아이디를 입력해주세요!")
        elif self.pw_input.get() == "":
            messagebox.showerror("입력 오류!", "비밀번호를 입력해주세요!")
        elif self.id_input.get() == "manager" and self.pw_input == "manager":
            # TODO 총 음료 판매 개수 및 수익 재고 경고 목록 띄우기
            # TODO 재고 경고 선택 가능하게 만들기
            messagebox.showinfo("환영합니다!", "어서오세요 매니저님!")
            return 0
        else:
            messagebox.showerror("로그인 오류!", "일치하는 정보가 없습니다!")

        return 1

        # Button(self, text="Go to page one",
        #        command=lambda: master.switch_frame(PageOne))
        # Button(self, text="Go to page two",
        #        command=lambda: master.switch_frame(PageTwo))


# class PageOne(Frame):
#     def __init__(self, master):
#         Frame.__init__(self, master)
#         Frame.configure(self, bg='blue')
#         Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
#         Button(self, text="Go back to start page",
#                command=lambda: master.switch_frame(LoginPage)).pack()
#
#
# class PageTwo(Frame):
#     def __init__(self, master):
#         Frame.__init__(self, master)
#         Frame.configure(self, bg='red')
#         Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
#         Button(self, text="Go back to start page",
#                command=lambda: master.switch_frame(LoginPage)).pack()


if __name__ == "__main__":
    app = SampleApp()
    app.title("Management System")
    app.mainloop()
