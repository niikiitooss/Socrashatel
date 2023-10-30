import sqlite3

connect = sqlite3.connect('database.db', check_same_thread=False)
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS "users"
("id" INTEGER NOT NULL,
"login" TEXT NOT NULL,
"password" TEXT NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "links"
("id" INTEGER NOT NULL,
"long" TEXT NOT NULL,
"short" TEXT NOT NULL,
"access_id" INTEGER NOT NULL,
"owner_id" INTEGER NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS "accesses"
("id" INTEGER NOT NULL,
"level_eng" TEXT NOT NULL,
"level_ru" TEXT NOT NULL,
primary key ("id" AUTOINCREMENT)
);''')
connect.commit()

#регистрация
def registration(login,password):
    cursor.execute('''INSERT INTO
        users (login,password)
        VALUES (?,?) 
        ''', (login,password,))
    connect.commit()

def searchUser(login):
    return cursor.execute('''SELECT password 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchone()

def searchUserId(login):
    return cursor.execute('''SELECT id 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchone()

def auth(login,password):
    cursor.execute('''SELECT * 
        FROM users
        WHERE login = ? 
        AND password = ?
        ''', (login, password,)).fetchone()
    return "Вы вошли"