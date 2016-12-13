__author__ = 'mmtbz'
import datetime

"""
this file has our local DB wich is MOCK_USERS which we will be using for a while
"""

MOCK_USERS = [{'email': 'mmtbz@qq.com',
               'salt': '8Fb23mMNHD5Zb8pr2qWA3PE9bH0=',
               'hashed': '1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876c'
                         'f0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e'}]

MOCK_TABLES = [{'_id': '1',
                'number': 1,
                'owner': 'mmtbz@qq.com',
                'url': 'http://127.0.0.1:5000/newtable/1'}]

MOCK_REQUEST = [{'_id': 1,
                 'table_number': 1,
                 'table_id': 1,
                 'time': datetime.datetime.now()}]


class MockDBHelper:
    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get('email') == email]
        if user:
            return user[0]
        return None

    # salt should be string, hashed also should be string
    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({'email': email, 'salt': salt, 'hashed': hashed})

    # add table to the database
    def add_table(self, number, owner):
        MOCK_TABLES.append({'_id': str(number), 'number': number, 'owner': owner})
        return number

    # after creating the URL then update the database
    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get("_id") == _id:
                table['url'] = url
                break

                # to get all tables

    def get_tables(self, owner_id):
        return MOCK_TABLES

    # loop throught the table list then check if there is a table with  the corresponding id
    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get('_id') == table_id:
                del MOCK_TABLES[i]
                break

    # get all request from database
    def get_request(self, owner_id):
        return MOCK_REQUEST

    # delete requests
    def delete_request(self, request_id):
        for i, req in enumerate(MOCK_REQUEST):
            if req.get('_id') == request_id:
                del MOCK_REQUEST[i]
                break

    # add request for the new user
    def add_request(self, tid):
        MOCK_REQUEST.append({'table_id': tid, 'time': datetime.datetime.now()})
