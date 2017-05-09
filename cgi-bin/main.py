#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe
# -*- coding: utf-8 -*-

import cgi
import html
import http.cookies
import os
import re

from engine import SessionNew
wall = SessionNew()

#     COOKIE
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
session = cookie.get("session")
if session is not None:
    session = session.value
    user = wall.find_cookie(session)  # шукаємо користувача по переданому печеньку
else:
    user = None


##########################################################################
##                                FORMS                                 ##
##########################################################################

bad_form = False
notific = ''
header = '...'
out = ''

regexp_nick = '^[a-zA-Z0-9]{1,20}$'
regexp_mail = "^([a-zA-Z\-0-9_\.']{1,64}@[a-zA-Z\-0-9_]{1,30}\.[a-zA-Z\-0-9_]{2,6})$"
regexp_passwd = '^[a-zA-Z0-9$%#\^@*&]{8,20}$'
regexp_age = '^([1][3-9])|([2-9][0-9])$'

#    LOGIN
form = cgi.FieldStorage()
login = form.getfirst("login", "")
login = html.escape(login)
password = form.getfirst("password", "")
password = html.escape(password)

#    CHANGE MAIL
change_mail_text = form.getfirst("change_mail", "")
change_mail_text = html.escape(change_mail_text)

#    CHANGE PASSWD
new_passwd = form.getfirst("new_passwd", "")
new_passwd = html.escape(new_passwd)
old_passwd = form.getfirst("old_passwd", "")
old_passwd = html.escape(old_passwd)

#    CHANGE AGE
new_age = form.getfirst("new_age", "")
new_age = html.escape(new_age)

#    DELETE ACC
delete_my_account = form.getfirst("delete_account", "")
delete_my_account = html.escape(delete_my_account)


#    Accept delete
__pass_for_delete = form.getfirst("passwd_for_delete", "")
__pass_for_delete = html.escape(__pass_for_delete)

#   Recovery
recovery_passwd = form.getfirst("email_recovery", "")
recovery_passwd = html.escape(recovery_passwd)

#           VALIDATION
if login != '' and password != '':
    if re.match(regexp_nick, login) or re.match(regexp_passwd, password):
        res = wall.find(login, password)
        if wall.find(login, password):
            cookie = wall.set_cookie(login)
            print('Set-cookie: session={}'.format(cookie))
            user = login
        else:
            bad_form = True
    else:
        bad_form = True
        notific = 'incorrect login or password'


elif change_mail_text != "":
    if not re.match(regexp_mail, change_mail_text):
        change_mail_text = ''
        notific = 'incorrect mail'
    else:
        notific = wall.change_mail(user, change_mail_text)


elif new_passwd != "" and old_passwd != "":
    if not re.match(regexp_passwd, new_passwd) or not \
            re.match(regexp_passwd, old_passwd):
        new_passwd, old_passwd = "", ''
        notific = 'incorrect password'
    else:
        notific = wall.change_passwd(user, new_passwd, old_passwd)


elif new_age != "":
    if not re.match(regexp_age, new_age):
        new_age = ''
        notific = 'incorrect age'
    else:
        notific = wall.change_age(user, new_age)

elif recovery_passwd != "":
    result = wall.forgot_passwd(recovery_passwd)
    if result != 'Error! Try again' and result:
        recovery_passwd = "OK"
    else:
        recovery_passwd = None



##########################################################################
##                              PTINTING                                ##
##########################################################################

file = open('cgi-bin/patterns/pattern.html', 'r')
pattern = file.read()


#       DELETING ACC
if __pass_for_delete != '':
    if wall.find(user, __pass_for_delete):
        if wall.delete_acc(user, __pass_for_delete):
            header = 'Account deleted'
            print('Set-cookie: session=; expires=Thu Jan 1 00:00:00 1970;')
            out = '''<p class='error'>Account has been deleted!
                        <br><a href="/">Login or Register</a>
                     <p>'''
    else:
        header = 'Account was not deleted'
        out = '''<p class='error'>Error. Try again!
                    <br><a href="/cgi-bin/main.py">Return on main</a>
                 <p>'''


#       COMMAND FOR DELITING
elif delete_my_account == "del_my_acc":
    header = 'Delete account'
    out = """<form action="main.py" method="post">
                <input type="password" size="40" name="passwd_for_delete" placeholder="Your password">
                <input class="but change" type="submit" value="Delete account">
            </form>"""


elif recovery_passwd is not None and recovery_passwd == "OK":
    header = "Message sent"
    out = "<p class='error'>Message sent. Check your email. " \
          "<br>[You can restore the page within 20 minutes]</p>"
    notific = "Message sent. Check your email"

#       OUT USER DATA
elif user is not None and not bad_form:
    header = 'Hello, '+user
    file = open('cgi-bin/patterns/user_data.html', 'r')
    all_data = wall.all_data_user(user)
    out = file.read()
    out = out.format(user_login=user, mail=all_data[2], age=all_data[3],
                     avatar='avatar.jpg')#all_data[4])

#       ERROR, BAD FORM
elif bad_form:
    header = 'Bad login'
    out = '''<p class='error'>Incorrect login or password 
                <br><a href="/">Try again</a>
             <p>'''

#       unauthorized
else:
    header = 'Bad login'
    out = '''<p class='error'>You are unauthorized, go to the login page!
                <br><a href="/">Go</a>
             <p>'''

#           OUT
print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=notific))