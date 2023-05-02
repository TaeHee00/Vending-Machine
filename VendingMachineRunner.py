from tkinter import *
# Pillow 패키지 내부의 PIL라이브러리를 사용하여 이미지 사용
from PIL import ImageTk
from tkmacosx import Button
# 데이터 관리를 손쉽게 하기 위해 json라이브러리 사용
import json

vm_window = Tk()
vm_window.title("자판기")
# 창의 초기 생성위치 설정
vm_window.config(padx=30, pady=20)
vm_window.geometry("+700+300")

# 가로 줄에 진열할 상품의 개수
row_limit = 5

imgSize = 64
img = ImageTk.PhotoImage(file="images/drink.png")
canvas_list = list()
label_list = list()
btn_list = list()
with open("drink_list.json", "r") as file:
    drink_list = json.load(file)
    column_cnt = 0
    row_cnt = 0
    for drink in drink_list:
        label_list.append(Label(text=drink))
        canvas_list.append(Canvas(width=imgSize, height=imgSize, highlightthickness=0))
        canvas_list[-1].create_image(imgSize/2, imgSize/2, image=img)
        if drink_list[drink]['재고'] > 0:
            btn_list.append(Button(text="●    구매가능", fg='green', focusthickness=0, activebackground='gray'))
            btn_list[-1]['state'] = 'normal'
        else:
            btn_list.append(Button(text="○    구매불가", disabledforeground='red', bg='gray'))
            btn_list[-1]['state'] = 'disabled'

        canvas_list[-1].grid(row=row_cnt, column=column_cnt)
        label_list[-1].grid(row=row_cnt + 1, column=column_cnt)
        btn_list[-1].grid(row=row_cnt + 2, column=column_cnt, padx=15)
        column_cnt += 1
        if column_cnt % row_limit == 0:
            Label(text=" ").grid(row=row_cnt + 3, column=column_cnt)
            Label(text=" ").grid(row=row_cnt + 4, column=column_cnt)
            Label(text=" ").grid(row=row_cnt + 5, column=column_cnt)
            column_cnt = 0
            row_cnt += 6

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
#         print("\n")
#
#         with open("drink_list.json", "w") as drink_list_file:
#             json.dump(data, drink_list_file, indent=4, ensure_ascii=False)