#! C:\Users\navch\AppData\Local\Programs\Python\Python35\python.exe
# -*- coding: utf-8 -*-

import os
import random
import time
import sqlite3
import hashlib
from random import choice
from string import ascii_letters

class DataBase:
    def __init__(self):
        self.name_db = 'site_db'
        self.__connect_to_db(self.name_db)
        self.__create_table_in_db()
        self.__close_db()

    def __connect_to_db(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor_db = self.conn.cursor()

    def __create_table_in_db(self):
        try:
            sql_stmt = '''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, nick VARCHAR,
                      mail VARCHAR, passwd VARCHAR, age INT, image VARCHAR default "avatar.jpg")'''
            self.cursor_db.execute(sql_stmt)
            sql_stmt = '''CREATE TABLE cookie (val VARCHAR PRIMARY KEY, nick VARCHAR)'''
            self.cursor_db.execute(sql_stmt)
            sql_stmt = '''CREATE TABLE recovery_passwd_page (name_page VARCHAR PRIMARY KEY, time_create FLOAT)'''
            self.cursor_db.execute(sql_stmt)
        except:
            return 1
        else:
            return 2

    def __close_db(self):
        self.cursor_db.close()
        self.conn.close()

    def __hash_passwd(self, passwd):
        h = hashlib.md5()
        h.update(passwd.encode("utf-8"))
        return h.hexdigest()

    def add_recovery(self, namefile):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''INSERT INTO main.recovery_passwd_page 
                    (name_page, time_create) VALUES (?,?)'''
        self.cursor_db.execute(sql_stmt, (namefile, time.time()))
        self.conn.commit()

    def get_recovery_page(self):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''SELECT * FROM main.recovery_passwd_page'''
        self.cursor_db.execute(sql_stmt)
        return self.cursor_db.fetchall()

    def del_recovery_page(self, name):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''DELETE FROM main.recovery_passwd_page WHERE name_page= ?'''
        self.cursor_db.execute(sql_stmt, (name,))
        self.conn.commit()
        self.__close_db()

    def add_new_user(self, login, mail, passwd):
        if not self.find_user(login) and not self.email_is_exist(mail):
            self.__connect_to_db(self.name_db)
            sql_stmt = '''INSERT INTO main.users (nick, mail, passwd) 
                                  VALUES (?,?,?)'''
            self.cursor_db.execute(sql_stmt, (login, mail,
                                              self.__hash_passwd(passwd)))
            self.conn.commit()
            self.__close_db()
            return True
        else:
            return False

    def find_user(self, login, passwd=None, return_all_data=False,
                  return_id=False, return_mail=False, return_passwd=False):
        try:
            self.__connect_to_db(self.name_db)
            sql_stmt = '''SELECT nick, passwd, mail, age, image, id FROM main.users WHERE nick=?'''
            self.cursor_db.execute(sql_stmt, (login,))
            result = self.cursor_db.fetchall()
            self.__close_db()
            if len(result) > 0:
                if passwd is not None:
                    return True if result[0][1] == self.__hash_passwd(passwd)\
                                                                else False
                elif return_all_data:
                    return result[0]
                elif return_id:
                    return result[0][5]
                elif return_mail:
                    return result[0][2]
                elif return_passwd:
                    return result[0][1]
                else:
                    return True
        except:
            return False


    def dump_cookie(self, cookie, user):
        self.__connect_to_db(self.name_db)
        sql_stmt = '''INSERT INTO main.cookie (val, nick) VALUES (?,?)'''
        self.cursor_db.execute(sql_stmt, (cookie, user))
        self.conn.commit()
        self.__close_db()

    def find_cookie(self, cookie):
        try:
            self.__connect_to_db(self.name_db)
            sql_stmt = '''SELECT nick FROM main.cookie WHERE val=?'''
            self.cursor_db.execute(sql_stmt, (cookie,))
            result = self.cursor_db.fetchall()
            self.__close_db()
        except:
            return False
        else:
            return result[0][0]

    def email_is_exist(self, mail, return_nick=False):
        try:
            self.__connect_to_db(self.name_db)
            sql_stmt = '''SELECT nick FROM main.users WHERE mail=?'''
            self.cursor_db.execute(sql_stmt, (mail,))
            result = self.cursor_db.fetchall()
            self.__close_db()
            if len(result) > 0:
                return True if not return_nick else result[0][0]
            else:
                return False
        except:
            return False

    def change_data(self, user, mail='', passwd='', age=0, avatar=''):
        try:
            if self.find_user(user):
                self.__connect_to_db(self.name_db)

                if mail != '':
                    sql_stmt = '''UPDATE main.users SET mail=? WHERE  nick=?'''
                    self.cursor_db.execute(sql_stmt, (mail, user))

                elif passwd != '':
                    sql_stmt = '''UPDATE main.users SET passwd=? WHERE nick=?'''
                    self.cursor_db.execute(sql_stmt,
                                           (self.__hash_passwd(passwd), user))

                elif age != 0:
                    sql_stmt = '''UPDATE main.users SET age=? WHERE nick=?'''
                    self.cursor_db.execute(sql_stmt, (age, user))

                elif avatar != '':
                    sql_stmt = '''UPDATE main.users SET image=? WHERE nick=?'''
                    self.cursor_db.execute(sql_stmt, (avatar, user))

                self.conn.commit()
                self.__close_db()
        except:
            return False
        else:
            return True

    def delete_acc(self, user):
        try:
            if self.find_user(user):
                self.__connect_to_db(self.name_db)
                sql_stmt = '''DELETE FROM main.users WHERE nick= ?'''
                self.cursor_db.execute(sql_stmt, (user,))
                self.conn.commit()
                self.__close_db()
        except:
            return False
        else:
            return True


class SessionNew:
    def __init__(self):
        self.db = DataBase()

    def register(self, user, mail, password):
        self.delete_recovery_page()
        return self.db.add_new_user(user, mail, password)

    def set_cookie(self, user):
        self.delete_recovery_page()
        cookie = str(time.time()) + str(random.randrange(10 ** 14))
        self.db.dump_cookie(cookie, user)
        return cookie

    def find_cookie(self, cookie):
        self.delete_recovery_page()
        return self.db.find_cookie(cookie)

    def find(self, user, password=None):
        self.delete_recovery_page()
        return self.db.find_user(user, password)

    def all_data_user(self, user):
        self.delete_recovery_page()
        return self.db.find_user(user, return_all_data=True)

    def change_mail(self, user, mail):
        self.delete_recovery_page()
        if not self.db.email_is_exist(mail):
            if self.db.change_data(user, mail=mail):
                return 'Mail has been changed'
            else:
                return 'Error. Try again'
        else:
            return 'This mail has already been'

    def change_passwd(self, user, new_passwd, old_passwd):
        if self.find(user, old_passwd):
            if self.db.change_data(user, passwd=new_passwd):
                return 'Password succesfully changed'
            else:
                return 'Error. Try again'
        else:
            return 'Wrong old password. Please try again'

    def change_age(self, user, new_age):
        if self.db.change_data(user, age=new_age):
            return 'Age has been changed'
        else:
            return 'Error. Try again'

    def delete_acc(self, user, passwd):
        if self.find(user, passwd):
            return self.db.delete_acc(user)
        else:
            return False

    def forgot_passwd(self, mail):
        self.delete_recovery_page()
        nick = self.db.email_is_exist(mail, True)
        if nick:
            name_temporary_page = ''.join(choice(ascii_letters)
                                          for i in range(30))
            # print(name_temporary_page+'.html')
            file = open('cgi-bin/patterns/pattern.html', 'r')
            pattern = file.read()
            header = 'Password Recovery'
            out = """<form action="/cgi-bin/recovery.py" method="post">
                        <!--<p>For the procedure was successful, do not change nickname</p>-->
                        <input type="text" size="40" name="nick_for_recovery" value='"""+nick+"""' style="display: none"> <br>
                        <input type="password" size="40" name="passwd_for_recovery" placeholder="Your new password">
                        <input class="but change" type="submit" value="Changed password">
                    </form>"""

            try:
                with open(name_temporary_page+'.html', 'w') as file:
                    file.write(pattern.format(title=header, content=out,
                                              notifications=''))
            except:
                return
            else:
                try:
                    # print(mail)
                    # print(name_temporary_page+'.html')
                    import smtplib
                    from email.mime.text import MIMEText

                    msg = MIMEText("Go to the password recovery: "
                                   "http://localhost:8000/"+
                                   name_temporary_page+'.html')

                    msg['Subject'] = 'Recovery passwd'
                    msg['From'] = 'softgroup@topnode.if.ua'
                    msg['To'] = mail

                    s = smtplib.SMTP('185.104.44.16', 25)
                    s.login('softgroup@topnode.if.ua', '3D8f1OuvOkL1')
                    s.send_message(msg)
                    s.quit()
                except:
                    return "Error send message"
                else:
                    self.db.add_recovery(name_temporary_page+'.html')
                    return True
        else:
            return False

    def __recovery(self, user, passwd):
        if self.db.change_data(user, passwd=passwd):
            return 'Password succesfully changed'
        else:
            return 'Error. Try again'

    def delete_recovery_page(self, del_now=False):
        result = self.db.get_recovery_page()
        max_time_for_recovery = 1200
        try:
            for i in result:
                print(i)
                if time.time() - i[1] > max_time_for_recovery or del_now:
                    os.remove(i[0])
                    self.db.del_recovery_page(i[0])
        except:
            return False


# ses = SessionNew()
# ses.forgot_passwd("navchalkin@gmail.com")
# # ses.db.change_data('navch', avatar='1.png')
# db = DataBase()
# print(db._DataBase__hash_passwd('itemud41'))
# # db.change_data('navch', avatar='1.png')
# db.add_new_user('miho', 'tr@ggh.com', 'passwd')
