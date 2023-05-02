from tkinter import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json

vm_window = Tk()
vm_window.title("자판기")
# 창의 초기 생성위치 설정
vm_window.geometry("+700+300")

imgSize = 64
img = ImageTk.PhotoImage(file="images/drink.png")
canvas = Canvas(width=imgSize, height=imgSize, highlightthickness=0)
canvas.create_image(32, 32, image=img)
canvas.grid(row=0, column=0)

tempButton1 = Button(text="임시 버튼1")
tempButton1.grid(row=1, column=0)


vm_window.mainloop()

# try:
#     with open("drink_list.json", "r") as drink_list_file:
#         data = json.load(drink_list_file)
#
# except FileNotFoundError:
#     with open("drink_list.json", "w") as drink_list_file:
#         data = {
#
#         }
#         json.dump(data, drink_list_file, indent=4)
#
# else:
#     while True:
#         drink_name = input("음료수 이름을 입력하세요: ")
#         if drink_name == "break":
#             break
#         drink_price = int(input("음료수 가격을 입력하세요: "))
#         drink_num = int(input("음료수 재고를 입력하세요: "))
#         new_data = {
#             drink_name: {
#                 "가격": drink_price,
#                 "재고": drink_num
#             }
#         }
#         data.update(new_data)
#
#         with open("drink_list.json", "w") as drink_list_file:
#             json.dump(data, drink_list_file, indent=4, ensure_ascii=False)