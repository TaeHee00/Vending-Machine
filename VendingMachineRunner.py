from tkinter import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk

vm_window = Tk()
vm_window.title("자판기")
# 창의 초기 생성위치 설정
vm_window.geometry("+700+300")

logoImg = ImageTk.PhotoImage(file="images/vending_machine.jpeg")
canvas = Canvas(width=176, height=286, highlightthickness=0)
canvas.create_image(int(176/2 + 1), int(286/2 + 1), image=logoImg)
canvas.grid(column=1, row=0)

vm_window.mainloop()