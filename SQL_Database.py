import sqlite3
from sqlite3 import Error

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
    cursor.execute('''DELETE FROM users WHERE name LIKE (?)''', (inputID,))
    db.commit()
    return cursor




#def main():
    #database = r"C:\Users\Arya\Desktop"
    database = r':memory:'

    # CREATE a database in file or RAM
    db = sqlite3.connect(database)

    cursor = createDB(db)

    name1 = 'AAPL'
    score1 = '1'
    udate1 = datetime.strftime(datetime.now()-timedelta(3), '%Y-%m-%d')
    updateDB(db, name1, score1, score1, udate1)

    name2 = 'GOOG'
    score2 = '4'
    udate2 = datetime.strftime(datetime.now()-timedelta(2), '%Y-%m-%d')
    updateDB(db, name2, score2, score2, udate2)

    name3 = 'ZM'
    score3 = '7'
    udate3 = date.today().strftime('%Y-%m-%d')
    updateDB(db, name3, score3, score3, udate3)

    print("GETTING ALL rows from db:")
    all_rows = getAllDB(cursor)
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns 2nd column (score)
        print('\t{0} : {1}: {2}: {3}'.format(row[0], row[1], row[2], row[3]))

    # UPDATE user with min score with new score
    row = getMinDBCorr(cursor)
    ticker = row[1]
    newscore = 5
    newdate = datetime.strftime(datetime.now() - timedelta(5), '%Y-%m-%d')
    updateDB(db, ticker, newscore, newscore, newdate)

    all_rows = getMaxDBCorr(cursor)
    print("RETRIEVING Max:")
    #for row in all_rows:
    print('\t{0} : {1}: {2}: {3}'.format(row[0], row[1], row[2], row[3]))


    #pdate = date.today().strftime('%Y-%m-%d')
    sdate = '2020-01-01'
    edate = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    all_rows = getPriorDB(cursor, sdate, edate)
    print("RETRIEVING Rows Prior to ", edate, ": ")
    #print(all_rows)
    for row in all_rows:
        print('\t{0} : {1}: {2}: {3}'.format(row[0], row[1], row[2], row[3]))

    db.close()

if __name__=="__main__":
    main()