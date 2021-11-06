"""
Filename: app.py

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/05/21
"""
from db_manager import *

if __name__ == '__main__':
    res = db_mgr.get_table_columns("test")

    print(res)

