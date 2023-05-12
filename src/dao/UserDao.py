class UserDao:

    def __init__(self, user_id, user_pw, user_name):
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name

    def getUserId(self):
        return self.user_id

    def getUserPw(self):
        return self.user_pw

    def getUserName(self):
        return self.user_name