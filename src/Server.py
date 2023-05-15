import json


class Server:

    def __init__(self, user_app):
        self.user_app = user_app
        self.user_app.amount_increase_btn_cash.configure(command=lambda: self.cash_injection_event())
        self.user_app.amount_return_btn.configure(command=lambda: self.cash_return_event())
        self.user_app.amount_increase_btn_card.configure(command=lambda: self.card_injection_event())

    def cash_return_event(self):
        # 결제 flag 초기화
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = ''
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # 투입금액이 있는지 확인
        if self.user_app.machine_amount <= 0:
            return

        # VMController에 현금 반환 요청
        self.user_app.vmController.cashReturn(self.user_app.temp_cash_cnt)
        # 반환된 Cash를 UserController에 Cash Injection 요청
        self.user_app.userController.cashReturn(self.user_app.user_seq, self.user_app.temp_cash_cnt)
        # cash ComboBox 객체 수정
        self.user_app.select_cash = self.user_app.amount_increase_combo.get().replace("원:", "").replace("개", "").split()
        select_cash_name = self.user_app.select_cash[0]
        idx = 0
        for _user_cash in self.user_app.user_cash_list:
            combo_cash_data = _user_cash.replace("원:", "").replace("개", "").split()
            combo_cash_name = combo_cash_data[0]
            self.user_app.user_cash_list[
                idx] = f"{combo_cash_name}원: {int(combo_cash_data[1]) + int(self.user_app.temp_cash_cnt[combo_cash_name])}개"
            idx += 1

        # ComboBox Update
        self.user_app.amount_increase_combo.config(values=self.user_app.user_cash_list)
        if "5000" == select_cash_name:
            self.user_app.amount_increase_combo.current(0)
        elif "1000" == select_cash_name:
            self.user_app.amount_increase_combo.current(1)
        elif "500" == select_cash_name:
            self.user_app.amount_increase_combo.current(2)
        elif "100" == select_cash_name:
            self.user_app.amount_increase_combo.current(3)
        # self.temp_cash_cnt 초기화
        for _cash in self.user_app.temp_cash_cnt:
            self.user_app.temp_cash_cnt[_cash] = 0
        self.user_app.temp_cash_cnt['total'] = 0
        # 투입 금액 label 초기화
        self.user_app.machine_amount_label.config(text=f"투입된 금액:\t{self.user_app.temp_cash_cnt['total']}원")
        # 음료 구매 버튼 수정
        for _drink in self.user_app.drink_content:
            # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
            _drink.state_btn['text'] = "○        구매불가"
            _drink.state_btn['fg'] = "red"
            _drink.state_btn['disabledforeground'] = "red"
            _drink.state_btn['state'] = "disabled"


