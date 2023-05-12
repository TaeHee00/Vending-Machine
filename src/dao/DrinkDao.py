class DrinkDao:

    def __init__(self, seq, drink_name, drink_price):
        self.seq = seq
        self.drink_name = drink_name
        self.drink_price = drink_price

    def getDrinkSeq(self):
        return self.seq

    def getDrinkName(self):
        return self.drink_name

    def getDrinkPrice(self):
        return self.drink_price