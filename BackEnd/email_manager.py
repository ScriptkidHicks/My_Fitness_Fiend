'''
code: email functionality
group: Wholesome as Heck Programmers
author(s): Thomas Joyce
last modified: 17 Nov 2021
'''
import random
import time
from db_manager import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_email(user_id):
    '''
    pass user_id as a string. 
    Will get user email and latest workout plan from database then call email()
    '''
    user_email_raw = db_mgr.get_one_row("users",["email"],\
                                 {"user_id": user_id})
    if user_email_raw:
        user_email = user_email_raw[0].strip()
        user_email += "@gmail.com"
    else:
        user_email = "test@gmail.com"
    user_plan_raw = db_mgr.get_one_row("workoutLogs",["details"],\
                                      {"user_id": user_id,\
                                       "user_has_completed": 0}, ["and"])
    if user_plan_raw:
        user_plan = []
        plan_list = user_plan_raw[0].strip("[]")
        plan_list = plan_list.replace("'", "")
        plan_list = plan_list.replace(" ", "")
        plan_list = plan_list.split(",")
        #print("here's the id's for the plan: {}".format(plan_list))
        for exercise in plan_list:
            workout_raw = db_mgr.get_one_row("workouts",["name"], \
                                        {"workout_id": exercise})
            if workout_raw:
                user_plan.append(workout_raw[0].strip())
            else:
                user_plan.append("workout not added")
    else:
        user_plan = ["test", "test", "test"]
    # print("end of get_email. Here's what I'm sending: ")
    # print("user_email: {}".format(user_email))
    # print("user_plan: {}".format(user_plan))
    email(user_email, user_plan)


def email(user_email, user_plan):
    '''


    to test enter in terminal: 

    python -m smtpd -c DebuggingServer -n localhost:1025

    if using a local debugging server, use localhost as SMTP server and use port 
    1025 rather than port 465. won’t need to use login() or encrypt the 
    communication using SSL. SSL (Secure Sockets Layer) is a protocol used to 
    encrypt an SMTP connection. It’s not necessary to use when using a local 
    debugging server.
    '''

    # email contents here
    sender_email = "fitnessfiend.dev@gmail.com"
    sender_pass = "fitnessfiend#1"
    receiver_email = user_email
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    Here is your workout plan for the day!
    {}
    To see your plan in more detail visit:
    http://www.FitnessFiends.com""".format(user_plan)
    html = """\
    <html>
    <body>
        <p>Hi,<br>
        Here is your workout plan for the day!<br>
        {}
        <a href="http://www.FitnessFiends.com">Fitness Fiends</a> 
        To see your plan in more detail visit:
        </p>
    </body>
    </html>
    """.format(user_plan)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    if localhost:
        port = 465 # For SSL
        smtp = "smtp.gmail.com"
    else:
        port = 1025 # for localhost
        smtp = "localhost"
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp, port, context=context) as server:
        if localhost:
            server.login(sender_email, sender_pass)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    localhost = True
    get_email("1")