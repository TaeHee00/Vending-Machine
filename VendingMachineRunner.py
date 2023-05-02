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
vm_window.geometry("+500+100")

# 가로 줄에 진열할 상품의 개수
row_limit = 5

# Canvas 내부에 들어갈 임시 이미지 크기
imgSize = 64
img = ImageTk.PhotoImage(file="images/drink.png")

# 음료가 추가될 경우 계속하여 객체를 만들어주어야 하기 때문에 관리의 편의성을 위해서
# 리스트 내부에 객체를 저장하여 사용
canvas_list = list()
label_list = list()
btn_list = list()

# drink_list.json 파일 내부 음료 목록을 불러와서 객체 생성
with open("drink_list.json", "r") as file:
    drink_list = json.load(file)

    # 음료 객체의 자리 배치에 사용하는 변수
    column_cnt = 0
    row_cnt = 0
    for drink in drink_list:
        label_list.append(Label(text=drink, font="Helvetica 12 bold"))
        canvas_list.append(Canvas(width=imgSize, height=imgSize, highlightthickness=0))
        # Canvas가 이미지 배치를 image의 중앙을 기준으로 배치함
        # imgSize / 2로 정렬
        canvas_list[-1].create_image(imgSize/2, imgSize/2, image=img)

        # 음료 재고에 따라 구매가능, 구매불가 판별
        if drink_list[drink]['재고'] > 0:
            btn_list.append(Button(text="●    구매가능", fg='green', focusthickness=0, activebackground='gray'))
            btn_list[-1]['state'] = 'normal'
        else:
            btn_list.append(Button(text="○    구매불가", disabledforeground='red', bg='gray'))
            btn_list[-1]['state'] = 'disabled'

        # 객체 생성
        canvas_list[-1].grid(row=row_cnt, column=column_cnt)
        label_list[-1].grid(row=row_cnt + 1, column=column_cnt)
        btn_list[-1].grid(row=row_cnt + 2, column=column_cnt, padx=15)

        column_cnt += 1
        Label(text=" ").grid(row=row_cnt + 3, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 4, column=column_cnt)
        Label(text=" ").grid(row=row_cnt + 5, column=column_cnt)
        if column_cnt % row_limit == 0:
            # 음료간의 간격 조정을 위해 빈 객체 생성, 배치
            column_cnt = 0
            row_cnt += 6

user_balance = 0
machine_balance = 0

# 자판기에 투입된 금액 표시
machine_balance_label = Label(text=f"투입된 금액:\t{machine_balance}원", font="Helvetica 16 bold")
# 가로로 진열할 음료의 개수가 3보다 적어도 오류가 발생하지 않도록 절대값을 사용
machine_balance_label.grid(row=99, column=abs(row_limit - 2), columnspan=3)

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