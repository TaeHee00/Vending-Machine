import json


class Server:

    def __init__(self, user_app):
        self.user_app = user_app
        self.user_app.amount_increase_btn_cash.configure(command=lambda: self.cash_injection_event())
        self.user_app.amount_return_btn.configure(command=lambda: self.cash_return_event())
        self.user_app.amount_increase_btn_card.configure(command=lambda: self.card_injection_event())

        # for content in self.user_app.drink_content:
            # TODO
            # content.state_btn.config(command=)

    def cash_decrease(self):
        pass

    def cash_injection_event(self):
        # 결제 할 수단을 cash로 변경
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = 'cash'
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # DB 연결 후 실시간 데이터 받아오기
        select_cash = self.user_app.amount_increase_combo.get().replace("원:", "").replace("개", "").split()
        cash_name = select_cash[0]
        # 선택한 지폐(화폐)가 1개 이상인지 확인
        if int(select_cash[1]) > 0:
            # User Cash decrease
            # TODO 카드 추가 기능 추가시 이부분 수정
            self.user_app.userController.userCashDecrease(self.user_app.user_seq, select_cash[0])
            # User Interface Cash decrease & Update
            idx = 0
            for user_cash in self.user_app.user_cash_list:
                if cash_name + "원" in user_cash:
                    self.user_app.user_cash_list[idx] = f"{cash_name}원: {int(select_cash[1]) - 1}개"
                    break
                idx += 1
            self.user_app.amount_increase_combo.configure(values=self.user_app.user_cash_list)
            if "5000원" in self.user_app.amount_increase_combo.get():
                self.user_app.amount_increase_combo.current(0)
                self.user_app.machine_amount += 5000
                self.user_app.temp_cash_cnt['total'] += 5000
            elif "1000원" in self.user_app.amount_increase_combo.get():
                self.user_app.amount_increase_combo.current(1)
                self.user_app.machine_amount += 1000
                self.user_app.temp_cash_cnt['total'] += 1000
            elif "500원" in self.user_app.amount_increase_combo.get():
                self.user_app.amount_increase_combo.current(2)
                self.user_app.machine_amount += 500
                self.user_app.temp_cash_cnt['total'] += 500
            elif "100원" in self.user_app.amount_increase_combo.get():
                self.user_app.amount_increase_combo.current(3)
                self.user_app.machine_amount += 100
                self.user_app.temp_cash_cnt['total'] += 100

            # temp_cash_cnt <- Cash Increase
            self.user_app.temp_cash_cnt[cash_name] += 1

            # VM Interface Cash Increase & Update
            self.user_app.machine_amount_label.config(text=f"투입된 금액:\t{self.user_app.temp_cash_cnt['total']}원",
                                                      font="Helvetica 16 bold")
            # Machine Cash Amount Increase
            self.user_app.vmController.managerCashInjection(cash_name)
            # 구매가능 음료 체크
            # 구매가능 음료 상태 변경
            for _drink in self.user_app.drink_content:
                # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
                if _drink.stock <= 0 or _drink.drink_price > self.user_app.temp_cash_cnt['total']:
                    _drink.state_btn['text'] = "○        구매불가"
                    _drink.state_btn['fg'] = "red"
                    _drink.state_btn['disabledforeground'] = "red"
                    _drink.state_btn['state'] = "disabled"
                else:
                    _drink.state_btn['text'] = "●        구매가능"
                    _drink.state_btn['fg'] = "green"
                    _drink.state_btn['state'] = "normal"

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

    # 카드 삽입시 잔액에 따라 구매 가능한 음료만 판매 상태 변경
    # 카드 삽입,제거시 투입된 금액 Label 변경
    # TODO 구매시 카드 잔액 실시간 업데이트
    # TODO 구매시 user_bag에 음료명: 개수 추가
    # TODO Manager 통계에서 판매 수익 및 판매 음료 추가
    def card_injection_event(self):
        # 결제 할 수단을 card로 변경
        with open("flag.json", "r") as file:
            flag_data = json.load(file)

        with open("flag.json", "w") as file:
            flag_data['flag'] = 'card'
            # TODO card_seq 가져오기
            flag_data['card_seq'] = ''
            json.dump(flag_data, file, indent=4)
        # 카드 삽입
        if self.user_app.amount_increase_btn_card['text'] == "카드 투입":
            self.user_app.amount_increase_btn_card['text'] = f"{self.user_app.cash_increase_combo.get().replace(':', '').split()[0]} 투입됨"
            self.user_app.amount_increase_btn_card['fg'] = "green"

            # TODO 카드잔액 코드 수정
            self.user_app.machine_amount_label['text'] = f"카드 잔액:\t{self.user_app.user_card[0].getCardAmount()}원"

            for _drink in self.user_app.drink_content:
                # TODO 판매 상태 세분화 ("재고 부족", "잔액 부족")
                if _drink.stock <= 0 or _drink.drink_price > int(self.user_app.user_card[0].getCardAmount()):
                    _drink.state_btn['text'] = "○        구매불가"
                    _drink.state_btn['fg'] = "red"
                    _drink.state_btn['disabledforeground'] = "red"
                    _drink.state_btn['state'] = "disabled"
                else:
                    _drink.state_btn['text'] = "●        구매가능"
                    _drink.state_btn['fg'] = "green"
                    _drink.state_btn['state'] = "normal"

        else:
            # 카드 제거
            # 결제 할 수단을 cash로 변경
            with open("flag.json", "r") as file:
                flag_data = json.load(file)

            with open("flag.json", "w") as file:
                flag_data['flag'] = ''
                flag_data['card_seq'] = ''
                json.dump(flag_data, file, indent=4)
            # TODO 카드 총 사용 내역 기능 추가 예정
            self.user_app.amount_increase_btn_card['text'] = "카드 투입"
            self.user_app.amount_increase_btn_card['fg'] = "black"

            for _drink in self.user_app.drink_content:
                _drink.state_btn['text'] = "○        구매불가"
                _drink.state_btn['disabledforeground'] = "red"
                _drink.state_btn['state'] = "disabled"

            self.user_app.machine_amount_label['text'] = f"투입된 금액:\t{self.user_app.temp_cash_cnt['total']}원"
