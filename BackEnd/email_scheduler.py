'''
code: email scheduling functionality
group: Wholesome as Heck Programmers
author(s): Thomas Joyce
last modified: 23 Nov 2021
ref:
    https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
    look here for scheduling daily sending functionality. 
'''

import time
import schedule
from email_manager import *

def get_users():
    users = db_mgr.get_all_rows("users", ["user_id"])
    for user in users:
        get_user(user[0])
        # print(str(user[0]))


schedule.every().day.at("8:30").do(get_users)

while True:
    schedule.run_pending()

get_users()