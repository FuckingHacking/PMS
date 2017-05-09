#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe
# -*- coding: utf-8 -*-

import cgi
import html

from engine import SessionNew
wall = SessionNew()


form = cgi.FieldStorage()
login = form.getfirst("nick_for_recovery", "")
login = html.escape(login)
password = form.getfirst("passwd_for_recovery", "")
password = html.escape(password)
out = ""

if login != '' and password != '':
    out = "<p class='error'>"+wall._SessionNew__recovery(login, password)+"</p><br><a href='/'>Go to login page</a>"
    msg = wall.delete_recovery_page(True)

else:
    out = "<p class='error'>Try again. Field must not be empty</p><br><a href='/'>Try again</a>"

file = open('cgi-bin/patterns/pattern.html', 'r')
pattern = file.read()
header = "result"

print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=''))