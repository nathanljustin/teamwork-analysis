# muddersOnRails()
# Sara McAllister November 5, 2017
# Last updated: 11-8-2017

# library for SQLite database calls for teamwork analysis app

import contextlib
import datetime
import sqlite3

DB = 'db/development.sqlite3'
test_DB = 'db/test.sqlite3'

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
def dbconnect(test):
    """Create cursor and ensure that DB connection closes"""
    sqlite_file = DB
    if test: sqlite_file = test_DB

    conn, cursor = connect(sqlite_file)
    try:
        yield cursor
    finally:
        close(conn)

def get_all_styles(test=False):
    """Return all style entries in db ordered based on entry in db"""
    with dbconnect(test) as c:
        scores = c.execute('SELECT * FROM styles').fetchall()
    return scores

def get_students_styles(student_ids, test=False):
    """Return style associated with a student's id"""
    placeholders = ', '.join('?' for id in student_ids)
    sql = 'SELECT * FROM styles WHERE student_id IN (%s)' % placeholders
    with dbconnect(test) as c:
        styles = c.execute(sql, student_ids).fetchall()
    return styles

def get_student_answers(student_id, test=False):
    """Return all answers associated with a student's id"""
    with dbconnect(test) as c:
        answers = c.execute(
            'SELECT * FROM answers WHERE student_id=? ORDER BY id DESC', 
            [student_id,],
        ).fetchall()
    return answers

def get_all_students(test=False):
    """Return all students' information"""
    with dbconnect(test) as c:
        students = c.execute('SELECT * FROM students').fetchall()
    return students

def get_all_student_IDs(test=False):
    """Return all students' information"""
    with dbconnect(test) as c:
        students = c.execute('SELECT id FROM students').fetchall()
    return students

def insert_student_team_pairs(student_and_team_ids, test=False):
    """Insert list of student_id team_id pairs into database"""
    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO assignments (student_id, team_id) VALUES (?,?)', 
            student_and_team_ids,
        )

def insert_students(students, test=False):
    """Insert list of new students into database"""
    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO students (name, created_at, updated_at, username) VALUES (?, ?, ?, ?);', 
            students,
        )

def insert_answers(values, student_ids, questions, test=False):
    """Insert list of new answers into database"""
    length = len(values)
    if not all(length == len(lst) for lst in [values, student_ids, questions]):
        raise ValueError('Inputs are not the same length')
    answers = [[values[i], student_ids[i], questions[i]] for i in range(len(values))]
    current_time = datetime.datetime.now().isoformat()

    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO answers (value, created_at, updated_at, student_id, question) VALUES (?, current_time, current_time, ?, ?);', 
            answers,
        )

def insert_styles(styles, test=False):
    """Insert list of new styles into database"""
    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO styles (student_id, communicator, collaborator, challenger, contributor, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);', 
            styles,
        )

