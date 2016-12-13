__author__ = 'mmtbz'
import hashlib
import os
import base64


class PasswordHelper:
    # get hash text from plain text
    def get_hash(self, plain):
        return hashlib.sha512(plain.encode()).hexdigest()

    def get_salt(self):
        return base64.b64encode(os.urandom(20))

# at this moment plain and salt are all string and stored in our database
    def validate_password(self, plain, salt, expected):
        return self.get_hash(plain + salt) == expected
