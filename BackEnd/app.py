"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/05/21
"""
from db_manager import *

if __name__ == '__main__':
    new_data = {
        "name": "James"
    }

    # db_mgr.add_row("test", new_data)

    res = db_mgr.get_one_row("test", ['id', 'name'])

    print(res)

