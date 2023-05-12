class VM_DrinkDao:

    def __init__(self, seq, drink_user_price, amount, state):
        self.seq = seq
        self.drink_user_price = drink_user_price
        self.amount = amount
        self.state = state

    def getDrinkSeq(self):
        return self.seq

    def getDrinkUserPrice(self):
        return self.drink_user_price

    def getAmount(self):
        return self.amount

    def getState(self):
        return self.state