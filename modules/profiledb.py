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

class Profile():

    def __init__(self, id, discord_id, tagline, fav_movie, fav_album, fav_game, switch, psn, xbl, battlenet, image):
        self.id = int(id)
        self.discord_id = int(discord_id)
        self.tagline = tagline
        self.fav_movie = fav_movie
        self.fav_album = fav_album
        self.fav_game = fav_game
        self.switch = switch
        self.psn = psn
        self.xbl = xbl
        self.battlenet = battlenet
        self.image = image

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
            tagline TEXT DEFAULT 'N/A',
            fav_movie TEXT DEFAULT 'N/A',
            fav_album TEXT DEFAULT 'N/A',
            fav_game TEXT DEFAULT 'N/A',
            switch TEXT DEFAULT 'N/A',
            psn TEXT DEFAULT 'N/A',
            xbl TEXT DEFAULT 'N/A',
            battlenet TEXT DEFAULT 'N/A',
            image TEXT DEFAULT 'N/A'
        );
    """
    con.execute(sqlInsertTableQuery)
    con.commit()

def CreateUser(con, uid):
    sqlInsertQuery = 'INSERT INTO USERS (discord_id) values(?)'
    data = [(uid,)]
    con.executemany(sqlInsertQuery, data)
    con.commit()

def ReadUser(con, id=None, uid=None, tagline=None, fav_movie=None, fav_album=None, fav_game=None, switch=None, psn=None, xbl=None, battlenet=None, image=None, limit=1):
    sqlReadQuery = "SELECT * FROM USERS WHERE"
    
    params = []

    if id != None:
        sqlReadQuery += " id=?"
        params.append(id)

    if uid != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " discord_id=?"
        params.append(uid)
    
    if tagline != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " tagline=?"
        params.append(tagline)

    if fav_movie != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " fav_movie=?"
        params.append(fav_movie)

    if fav_album != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " fav_album=?"
        params.append(fav_album)

    if fav_game != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " fav_game=?"
        params.append(fav_game)

    if switch != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " switch=?"
        params.append(switch)

    if psn != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " psn=?"
        params.append(psn)    
    
    if xbl != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " xbl=?"
        params.append(xbl)

    if battlenet != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " battlenet=?"
        params.append(battlenet)

    if image != None:
        if len(params) > 0:
            sqlReadQuery += " AND"
        sqlReadQuery += " image=?"
        params.append(image)

    if len(params) == 0:
        return

    sqlReadQuery += ";"
    sqlQueryResults = con.execute(sqlReadQuery, tuple(params))

    data = []
    count = 0;

    for row in sqlQueryResults:

        profile = Profile(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
        if limit == 1:
            return profile

        data.append(profile)
        count += 1

        if count >= limit:
            return data

    if len(data) == 0:
        return None
    else:
        return data

def UpdateUser(con, profile):
    
    sqlUpdateQuery = "UPDATE USERS SET discord_id=?, tagline=?, fav_movie=?, fav_album=?, fav_game=?, switch=?, psn=?, xbl=?, battlenet=?, image=? WHERE id=?"
    data = (profile.discord_id, profile.tagline, profile.fav_movie, profile.fav_album, profile.fav_game, profile.switch, profile.psn, profile.xbl, profile.battlenet, profile.image, profile.id)
    con.execute(sqlUpdateQuery, data)
    con.commit()

def DeleteUser(con, id):

    sqlDeleteQuery = "DELETE FROM USERS WHERE id=?"
    data = (id,)
    con.execute(sqlDeleteQuery, data)
    con.commit()

if __name__ == '__main__':
    con = sl.connect('test.db')
    InitializeProfileDatabase(con, True)
    CreateUser(con, 1234567890)
    u = ReadUser(con, uid=1234567890)
    print(u.discord_id)
    u.discord_id = 5555555555
    UpdateUser(con, u)
    u = ReadUser(con, id=u.id)
    print(u.discord_id)
    DeleteUser(con, id=u.id)