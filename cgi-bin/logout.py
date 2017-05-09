#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe

import os
import http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
name = cookie.get("session")

file = open('cgi-bin/patterns/pattern.html', 'r')
pattern = file.read()


if name is not None:
    print('Set-cookie: session=; expires=Thu Jan 1 00:00:00 1970;')
    header = 'Logout'
    out = '''<p class='error'>Exited! 
                <br><a href="/">Login or Register</a>
             <p>'''
else:
    header = 'Logout'
    out = '''<p class='error'>You have not entered! 
                <br><a href="/">Login or Register</a>
             <p>'''


print('Content-type: text/html\n')
print(pattern.format(title=header, content=out, notifications=''))