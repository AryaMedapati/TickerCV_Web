import sqlite3
from sqlite3 import Error

def startFbDb(path):
    database = path
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
    return cursor

def updateFbDb(db, name, comment, cdate):
    # Get a cursor object
    cursor = db.cursor()
    cursor.execute('''INSERT or REPLACE INTO feedback(name, comment, cdate)
                    VALUES(?,?,?)''', (name, comment, cdate))
    db.commit()
    return cursor

def getAllFbDb(cursor):
    #cursor.execute('''SELECT id, name, comment, cdate FROM feedback''')
    cursor.execute('''SELECT * FROM feedback ORDER by id DESC''')
    all_rows = cursor.fetchall()
    return all_rows

def getRecentFbDb(cursor, limit):
    cursor.execute('''SELECT * FROM feedback ORDER by id DESC LIMIT (?)''', (limit,))
    all_rows = cursor.fetchall()
    return all_rows

def deleteFb(db, inputID):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM feedback WHERE id = (?)''', (inputID,))
    db.commit()
    return cursor