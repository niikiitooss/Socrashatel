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
"count" INT NOT NULL,
"access_id" INTEGER NOT NULL,
"user_id" INTEGER NOT NULL,
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

def registr(login,password):
    cursor.execute('''INSERT INTO
        users (login,password)
        VALUES (?,?) 
        ''', (login,password))
    connect.commit()

def auth(login,password):
    cursor.execute('''SELECT * 
        FROM users
        WHERE login = ? 
        AND password = ?
        ''', (login, password,)).fetchone()
    return "Вы вошли"

def getUser(login):
    return cursor.execute('''SELECT password 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchall()

def getUserId(login):
    return cursor.execute('''SELECT id 
        FROM users
        WHERE login = ? 
        ''', (login,)).fetchone()

def addLink(long,short,access_id,user_id,count = 0):
    cursor.execute('''INSERT INTO
        links (long,short,count,access_id,user_id)
        VALUES (?,?,?,?,?)
        ''', (long,short,count,access_id,user_id))
    connect.commit()

def getAccesses():
    return cursor.execute('''SELECT * FROM accesses
    ''',()).fetchall()

def addAccesses(level_eng,level_ru):
    cursor.execute('''INSERT INTO
        accesses (level_eng,level_ru)
        VALUES (?,?)
        ''', (level_eng,level_ru))
    connect.commit()
    return "Добавление категории прошло успешно"

def getUserLinks(user_id):
    return cursor.execute('''SELECT links.long, links.short, links.count, accesses.level_ru, accesses.id
    FROM links
    INNER JOIN accesses ON accesses.id = links.access_id
    WHERE links.user_id = ?
    ''', (user_id,)).fetchall()

def getPseudonym(pseudonym):
    return cursor.execute('''SELECT short 
    FROM links
    WHERE short = ?''',(pseudonym,)).fetchall()

def getLongUser(long_link, user_id):
    return cursor.execute('''SELECT long 
    FROM links
    WHERE long = ? AND user_id = ?''',(long_link,user_id)).fetchall()

def getInfoLink(user_id, long_link):
    return cursor.execute('''SELECT long, short, count, access_id
    FROM links 
    WHERE user_id = ? AND long = ?''',(user_id,long_link)).fetchall()

def updateLink(long,short,access_id,user_id):
    cursor.execute('''UPDATE links
    SET short = ?, access_id = ?
    WHERE user_id = ? AND long = ?''',(short,access_id,user_id,long))
    connect.commit()

def deleteLink(long_link, user_id):
    cursor.execute('''DELETE
    FROM links
    WHERE long = ? AND user_id = ?''',(long_link,user_id))
    connect.commit()
    return "Удалил"

def getLinkInfo(short):
    return cursor.execute('''SELECT long, count, access_id, user_id
    FROM links
    WHERE short = ?''',(short,)).fetchall()

def updateCount(long,count):
    cursor.execute('''UPDATE links
    SET count = ?
    WHERE long = ?''',(count,long))
    connect.commit()

def accessesInfo():
    return cursor.execute('''SELECT level_ru
    FROM accesses''').fetchall()