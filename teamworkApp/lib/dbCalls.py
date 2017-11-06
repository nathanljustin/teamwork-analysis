# muddersOnRails()
# Sara McAllister November 5, 2-17
# Last updated: 11-5-2017

# library for SQLite database calls for teamwork analysis app

import contextlib
import sqlite3

DB = 'db/development.sqlite3'

def connect(sqlite_file):
    """ Make connection to an SQLite database file """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c

def close(conn):
    """ Commit changes and close connection to the database """
    conn.commit()
    conn.close()

@contextlib.contextmanager
def dbconnect(sqlite_file=DB):
  conn, cursor = connect(sqlite_file)
  try:
    yield cursor
  finally:
    close(conn)

def getAllStyles():
    """Get all style entries in db ordered based on entry in db"""
    with dbconnect() as cursor:
        scores = cursor.execute('SELECT * FROM styles').fetchall()
    return scores