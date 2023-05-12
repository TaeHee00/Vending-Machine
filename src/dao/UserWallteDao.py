class UserWallteDao:

    def __init__(self, user_seq, cash_card_seq, flag):
        self.user_seq = user_seq
        self.cash_card_name = cash_card_seq
        self.flag = flag

    def getUserSeq(self):
        return self.user_seq

    def getCashCardSeq(self):
        return self.cash_card_seq

    def getFlag(self):
        return self.flag