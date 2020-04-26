import sqlite3
from sqlite3 import Error

def startFbDb():
    database = '/home/aryam/mysite/feedback.db'
    #database = r':memory:'
    # CREATE a database in file or RAM
    db = sqlite3.connect(database)
    return db

def createFbDb(db):
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY, name TEXT , comment TEXT, cdate DATE)
        ''')
    db.commit()
    cursor = db.cursor()
    return cursor

def updateFbDb(db, name, comment, cdate):
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''INSERT or REPLACE INTO feedback(name, comment, cdate)
                    VALUES(?,?,?)''', (name, comment, cdate))
    db.commit()
    return cursor

def getAllFbDb(cursor):
    cursor.execute('''SELECT name, comment, cdate FROM feedback''')
    all_rows = cursor.fetchall()
    return all_rows

def getRecentFbDb(cursor, limit):
    cursor.execute('''SELECT * FROM feedback ORDER by id DESC LIMIT (?)''', (limit,))
    all_rows = cursor.fetchall()
    return all_rows
