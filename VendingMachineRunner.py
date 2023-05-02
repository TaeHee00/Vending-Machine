from tkinter import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json

vm_window = Tk()
vm_window.title("자판기")
vm_window.config()
# 창의 초기 생성위치 설정
vm_window.geometry("+700+300")

logoImg = ImageTk.PhotoImage(file="images/vending-machine.png")
vmImageSize = 256
canvas = Canvas(width=vmImageSize, height=vmImageSize, highlightthickness=0)
canvas.create_image(int(vmImageSize/2 + 1), int(vmImageSize/2 + 1), image=logoImg)
canvas.grid(column=2, row=0)

tempButton1 = Button(text="임시 버튼1")
tempButton1.grid(column=0, row=1)
tempButton2 = Button(text="임시 버튼2")
tempButton2.grid(column=1, row=1)
tempButton3 = Button(text="임시 버튼3")
tempButton3.grid(column=2, row=1)
tempButton4 = Button(text="임시 버튼4")
tempButton4.grid(column=3, row=1)
tempButton5 = Button(text="임시 버튼5")
tempButton5.grid(column=4, row=1)


vm_window.mainloop()