__author__ = 'mmtbz'
import base64
import os
import hashlib

MOCK_USERS = [{'email': 'mmtbz@qq.com',
               'salt': '8Fb23mMNHD5Zb8pr2qWA3PE9bH0=',
               'hashed': '1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876c'
                         'f0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e'}]
def get_salt():
    return base64.b64encode(os.urandom(20))


def get_hash(plain):
    return hashlib.sha512(plain.encode()).hexdigest()


def add_user(email, salt, hashed):
    MOCK_USERS.append({'email': email, 'salt': salt, 'hashed': hashed})


def main():
    plain = '123456'

    add_user(email='mm@qq.com', salt='GHKSGSVDGDBBDHDH', hashed='45678909876574')

    print(MOCK_USERS[1])
main()
