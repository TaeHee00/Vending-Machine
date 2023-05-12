class CardDao:

    def __init__(self, seq, card_name, amount):
        self.seq = seq
        self.card_name = card_name
        self.amount = amount

    def getCardSeq(self):
        return self.seq

    def getCardName(self):
        return self.card_name

    def getCardAmount(self):
        return self.amount