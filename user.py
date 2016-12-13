__author__ = 'mmtbz'
""""
This is a class for  users, check their username, password and so on
"""


class User:
    def __init__(self, email):
        self.email = email

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def is_authenticated(self):
        return True
