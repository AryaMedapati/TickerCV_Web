import sqlite3
from sqlite3 import Error

# Get a cursor object
def createPDB(db):
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
    return cursor

# INITIALLIZE DB (called users) with 2 entries
def updatePDB(db, name):
    cursor = db.cursor()
    cursor.execute('''INSERT or REPLACE INTO users(name)
                    VALUES(?)''', (name,))
    db.commit()
    return cursor

def getRow0PDB(cursor):
    cursor.execute('''SELECT name FROM users''')
    row = cursor.fetchone()
    return row
