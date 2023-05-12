class CashDao:

    def __init__(self, seq, cash_name, amount):
        self.seq = seq
        self.cash_name = cash_name
        self.amount = amount

    def getCashSeq(self):
        return self.seq

    def getCashName(self):
        return self.cash_name

    def getCashAmount(self):
        return self.amount
