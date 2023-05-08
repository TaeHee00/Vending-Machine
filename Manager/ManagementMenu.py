from tkinter import *


def drink_page():
    window.destroy()
    from Manager import DrinkManager
    DrinkManager.DrinkManager()


class ManagementMenu:
    global window
    window = Tk()
    window.title("Management Menu")
    window.config(padx=15, pady=15)
    window.geometry("+450+300")
    window.resizable(False, False)

    # 음료수 재고 관리 이동 버튼
    # TODO User Interface와 동일한 화면 구성에서 구매 버튼 대신 재고 추가 버튼 생성
    # TODO 재고관리 마무리할 경우 마지막 재고 추가에 따른 음료 구매 금액 청구 (판매 금액의 50%)

    drink_management = Button(text="음료 재고 관리", command=drink_page)
    drink_management.grid(row=0, column=0, padx=2)

    # 현금 재고 관리 이동 버튼
    cash_management = Button(text="현금 재고 관리")
    cash_management.grid(row=0, column=1, padx=2)

    # 판매 정산 정보 이동 버튼
    sales_settlement = Button(text="판매 정산 정보")
    sales_settlement.grid(row=0, column=2, padx=2)

    # 재고 경고 관리 이동 버튼
    stock_alert = Button(text="재고 경고 관리")
    stock_alert.grid(row=0, column=3, padx=2)

    # 판매 통계 정보 이동 버튼
    sales_statistics = Button(text="판매 통계 정보")
    sales_statistics.grid(row=0, column=4, padx=2)

    window.mainloop()
