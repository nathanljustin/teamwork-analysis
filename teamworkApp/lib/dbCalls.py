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
    """Create cursor and ensure that DB connection closes"""
    conn, cursor = connect(sqlite_file)
    try:
        yield cursor
    finally:
        close(conn)

def get_all_styles():
    """Return all style entries in db ordered based on entry in db"""
    with dbconnect() as c:
        scores = c.execute('SELECT * FROM styles').fetchall()
    return scores

def get_student_styles(student_id):
    """Return style associated with a student's id"""
    with dbconnect() as c:
        styles = c.execute(
            'SELECT * FROM styles WHERE student_id=?', 
            [student_id,],
        ).fetchall()
    return styles

def get_student_answers(student_id):
    """Return all answers associated with a student's id"""
    with dbconnect() as c:
        answers = c.execute(
            'SELECT * FROM answers WHERE student_id=? ORDER BY id DESC', 
            [student_id,],
        ).fetchone()
    return answers

def get_all_students():
    """Return all students' information"""
    with dbconnect() as c:
        students = c.execute('SELECT * FROM students').fetchall()
    return students

def get_all_student_IDs():
    """Return all students' information"""
    with dbconnect() as c:
        students = c.execute('SELECT id FROM students').fetchall()
    return students

def insert_student_team_pairs(student_and_team_ids):
    """Insert list of student_id team_id pairs into database"""
    with dbconnect() as c:
        c.executemany(
            'INSERT INTO assignments (student_id, team_id) VALUES (?,?)', 
            student_and_team_ids,
        )

def insert_students(students):
    """Insert list of new students into database"""
    with dbconnect() as c:
        c.executemany(
            'INSERT INTO students (name, created_at, updated_at, username) VALUES (?, ?, ?, ?);', 
            student_to_db,
        )

def insert_answers(answers):
    """Insert list of new answers into database"""
    with dbconnect() as c:
        c.executemany(
            'INSERT INTO answers (value, created_at, updated_at, student_id, question) VALUES (?, ?, ?, ?, ?);', 
            answers,
        )

def insert_styles(styles):
    """Insert list of new styles into database"""
    with dbconnect() as c:
        c.executemany(
            'INSERT INTO styles (student_id, communicator, collaborator, challenger, contributor, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);', 
            styles,
        )

