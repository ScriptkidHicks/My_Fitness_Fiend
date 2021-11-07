"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/07/21
"""
from db_manager import db_mgr

if __name__ == '__main__':
    # db_mgr.delete_rows('users')

    # data = {
    #     'email': 'my_other_email@email.com',
    #     'first_name': 'Me',
    #     'last_name': 'MEEEE',
    #     'full_name': 'Me MEEEE',
    #     'password': 'password123'
    # }

    # db_mgr.add_one_row('users', data)

    db_results = db_mgr.get_all_rows('users',
                                     ['user_id'],
                                     where_options={'email': 'my_other_email@email.com',
                                                    'password': 'password123'},
                                     where_connectors=['AND'])
                                        

    print(db_results[0][0])

    # res = db_mgr.get_all_rows('users', ['*'])
    # print(res)


