import pymysql
import os
import sys



sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from repository.Repository import Repository
from repository.CardRepository import CardRepository
from repository.CashRepository import CashRepository


# TODO dao에서 객체로 변경
class UserRepository(Repository):

    def __init__(self):
        super().__init__()

    def find(self):
        self.query = "SELECT * FROM user"
        self.cursor.execute(self.query)
        self.result = self.cursor.fetchall()
        return self.result

    # TODO 회원가입 기능
    # 기본 현금 및 카드 생성
    def save(self, userDao):
        self.query = "INSERT INTO user (user_id, user_pw, user_name) VALUES (%s, %s, %s)"
        data = (userDao.getUserId(), userDao.getUserPw(), userDao.getUserName())
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "SELECT * FROM user WHERE user.user_id = (%s)"
        data = (userDao.getUserId())
        self.cursor.execute(self.query, data)
        self.result = self.cursor.fetchone()
        user_seq = self.result[0]

        # DEFAULT CARD DATA INSERT
        self.query = "INSERT INTO card (card_name, amount) VALUES (%s, %s)"
        data = ('농협카드', '20000')
        self.cursor.execute(self.query, data)
        self.db.commit()

        # DEFAULT CASH DATA INSERT
        self.query = "INSERT INTO cash (cash_name, amount) VALUES (%s, %s)"
        data = ('5000', '3')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO cash (cash_name, amount) VALUES (%s, %s)"
        data = ('1000', '5')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO cash (cash_name, amount) VALUES (%s, %s)"
        data = ('500', '10')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO cash (cash_name, amount) VALUES (%s, %s)"
        data = ('10', '10')
        self.cursor.execute(self.query, data)
        self.db.commit()

        cardRepository = CardRepository()
        new_card = cardRepository.findCreateCard()
        cashRepository = CashRepository()
        new_cash = cashRepository.findCreateCash()

        # SYNC WALLET - CARD
        self.query = "INSERT INTO user_wallte (user_seq, card_seq, flag) VALUES (%s, %s, %s)"
        data = (user_seq, new_card[0], 'card')
        self.cursor.execute(self.query, data)
        self.db.commit()

        # SYNC WALLET - CASH
        self.query = "INSERT INTO user_wallte (user_seq, cash_seq, flag) VALUES (%s, %s, %s)"
        data = (user_seq, new_cash[0][0], 'cash')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO user_wallte (user_seq, cash_seq, flag) VALUES (%s, %s, %s)"
        data = (user_seq, new_cash[1][0], 'cash')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO user_wallte (user_seq, cash_seq, flag) VALUES (%s, %s, %s)"
        data = (user_seq, new_cash[2][0], 'cash')
        self.cursor.execute(self.query, data)
        self.db.commit()

        self.query = "INSERT INTO user_wallte (user_seq, cash_seq, flag) VALUES (%s, %s, %s)"
        data = (user_seq, new_cash[3][0], 'cash')
        self.cursor.execute(self.query, data)
        self.db.commit()



    # TODO 유저 정보 수정
    def update(self):
        pass

    # TODO 유저 정보 삭제
    def delete(self):
        pass