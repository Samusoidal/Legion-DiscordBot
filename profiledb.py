## Sam :)
## Created 10-07-21

## ---- profiledb.py ----
# 
# Provides methods to interact with a sqlite database for storing user profiles
#
# Requirements:
# - sqlite3
#
## --------------------


import sqlite3 as sl


## ---------------------
### Data Access Objects
## ---------------------

## ---------------------
### Database Operations
## ---------------------

def InitializeProfileDatabase(con, force=False):

    cursor = con.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='USERS';""")

    if cursor.fetchone() is not None:
        if force:
            sqlDeleteTableQuery = """
                DROP TABLE USERS;
            """
            con.execute(sqlDeleteTableQuery)
        else:
            return

    sqlInsertTableQuery = """
        CREATE TABLE USERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            discord_id LONG,
            pronouns TEXT DEFAULT 'N/A',
            switch_fc TEXT DEFAULT 'N/A',
            psn TEXT DEFAULT 'N/A',
            xbl TEXT DEFAULT 'N/A',
            battlenet TEXT DEFAULT 'N/A',
            image TEXT DEFAULT 'N/A'
        );
    """
    con.execute(sqlInsertTableQuery)
    con.commit()

def CreateUser(con, uid):
    sql = 'INSERT INTO USERS (discord_id) values(?)'
    data = [(uid,)]
    con.executemany(sql, data)
    con.commit()

def ReadUser(con, uid):
    data = con.execute("SELECT * FROM USERS WHERE discord_id = " + str(uid))
    for row in data:
        print(row)

if __name__ == '__main__':
    con = sl.connect('test.db')
    InitializeProfileDatabase(con, True)
    CreateUser(con, 1234567890)
    ReadUser(con, 1234567890)