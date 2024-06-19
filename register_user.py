import sqlite3
from getpass import getpass
import bcrypt

DATABASE = 'users.db'

db = sqlite3.connect(DATABASE)

cursor = db.cursor()

try:
    cursor.execute("""CREATE TABLE user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) NOT NULL UNIQUE,
        password VARCHAR(180) NOT NULL);""")
except sqlite3.OperationalError:
    print('The table exists already, ignoring CREATE command.')

print('\033[0;35m='*20+' REGISTER ADMIN USER '+'='*20+'\033[0;0m')
username = input('\033[0;33m>> USERNAME : ')
password = bcrypt.hashpw(
    getpass('\033[0;33m>> PASSWORD : \033[0;0m').encode('utf-8'), bcrypt.gensalt())

try:
    cursor.execute(
        rf"""INSERT INTO user (username, password) VALUES ("{username}", "]={password}")""")

    print('\033[0;35m[REGISTER] admin user registered into database.\033[0;0m')
except Exception as e:
    print(e)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IF YOU EVER NEED TO CHECK THE DATABASE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# cursor.execute("SELECT * FROM user")
# print(cursor.fetchall())

db.commit()
db.close()
