#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe
# -*- coding: utf-8 -*-

import cgi
import html

from engine import SessionNew
wall = SessionNew()


form = cgi.FieldStorage()
login = form.getfirst("login_reg", "")
login = html.escape(login)
mail = form.getfirst("email_reg", "")
mail = html.escape(mail)
password = form.getfirst("password_reg", "")
password = html.escape(password)

out = " ".join((login, mail, password))

if login != '' and mail != '' and password != '':
    if not wall.find(login):
        if wall.register(login, mail, password):
            out = '''<p class='error'>Register has been succesfully. 
                        <br><a href="/">Go to login page</a>
                     <p>'''
        else:
            out = '''<p class='error'>This mail was used. 
                        <br><a href="/">Try again</a>
                     <p>'''

    else:
        out = '''<p class='error'>This nickname is exist. 
                    <br><a href="/">Try again</a>
                 <p>'''
else:
    out = '''<p class='error'>Do not leave empty fields. 
                <br><a href="/">Try again</a>
             <p>'''


file = open('cgi-bin/patterns/pattern.html', 'r')
pattern = file.read()

header = 'register'

print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=''))