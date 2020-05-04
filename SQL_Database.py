import datetime
from datetime import date, timedelta

# Get a cursor object
def createDB(db):
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT UNIQUE,
    corrscore FLOAT, rsiscore FLOAT, udate DATE)''')
    return cursor

# INITIALLIZE DB (called users) with 2 entries
def updateDB(db, name, corrscore, rsiscore, udate):
    cursor = db.cursor()
    cursor.execute('''INSERT or REPLACE INTO users(name, corrscore, rsiscore, udate)
                    VALUES(?,?,?,?)''', (name, corrscore, rsiscore, udate))
    db.commit()
    return cursor



def getRow0DB(cursor):
    cursor.execute('''SELECT name, corrscore, rsiscore, udate FROM users''')
    row = cursor.fetchone()
    return row

    #SEARCH for MAX
def getAllDB(cursor):
    cursor.execute('''SELECT name, corrscore, rsiscore, udate FROM users''')
    all_rows = cursor.fetchall()
    return all_rows
    # for row in all_rows:
    # row[0] returns the first column in the query (name), row[1] returns 2nd column (score)
    #     return print('{0} : {1}'.format(row[0], row[1]))

def getTopCorr(cursor):
    cursor.execute('''SELECT name, corrscore, rsiscore, udate FROM users ORDER BY corrscore DESC LIMIT 10;''')
    all_rows = cursor.fetchall()
    #print("Top 5 Correlation")
    #print(all_rows)
    return all_rows

def getToprsi(cursor):
    cursor.execute('''SELECT name, corrscore, rsiscore, udate FROM users ORDER BY rsiscore DESC LIMIT 10;''')
    all_rows = cursor.fetchall()
    #print("Top 5 rsisCores")
    #print(all_rows)
    return all_rows

# UPDATE user with MAX score with new MAX score
def getMaxDBCorr(cursor):
    cursor.execute('''SELECT name, max(corrscore), rsiscore, udate FROM users''')
    row = cursor.fetchone()
    return row

def getMaxDBrsi(cursor):
    cursor.execute('''SELECT name, corrscore, max(rsiscore), udate FROM users''')
    row = cursor.fetchone()
    return row

def getMinDBCorr(cursor):
    cursor.execute('''SELECT name, min(corrscore), rsiscore, udate FROM users''')
    row = cursor.fetchone()
    return row

def getMinDBrsi(cursor):
    cursor.execute('''SELECT name, corrscore, min(rsiscore), udate FROM users''')
    row = cursor.fetchone()
    return row

def getPriorDB(cursor, sdate, edate):
    cursor.execute('''SELECT * FROM users WHERE
    strftime('%s', udate) BETWEEN strftime('%s', ?) AND strftime('%s', ?)''', (sdate, edate))
    all_rows = cursor.fetchall()
    return all_rows

def deleteDB(db, inputID):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM users WHERE name = (?)''', (inputID,))
    db.commit()
    return cursor




