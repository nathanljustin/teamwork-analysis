# muddersOnRails()
# Sara McAllister November 5, 2017
# Last updated: 11-8-2017

# library for SQLite database calls for teamwork analysis app

import contextlib
import datetime
import sqlite3

# rails creates databases of these names
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
    """Create a curser that will always close the connection"""

    # choose database (default is normal DB)
    sqlite_file = DB
    if test: sqlite_file = test_DB

    # create cursor and give to function
    conn, cursor = connect(sqlite_file)
    try:
        yield cursor
    # always commit and close connection
    finally:
        close(conn)

###########################################
#                Getters                  #
###########################################

def get_all_styles(test=False):
    """
    Return all style entries in db ordered based on entry in db

    Returns:
        List of style entries (essentially list of tuples)
    """
    with dbconnect(test) as c:
        scores = c.execute('SELECT * FROM styles').fetchall()
    return scores


def get_students_styles(student_ids, test=False):
    """
    Return style associated with students' ids

    Args:
        student_ids: A list of student_ids 

    Returns:
        List of style db entries
    """
    placeholders = ', '.join('?' for id in student_ids)
    sql = 'SELECT * FROM styles WHERE student_id IN (%s)' % placeholders
    with dbconnect(test) as c:
        styles = c.execute(sql, student_ids).fetchall()
    return styles

def get_name(student_id, test=False):
    """
    """
    with dbconnect(test) as c:
        name = c.execute(
            'SELECT name FROM students WHERE id =?', 
            [student_id,],
        ).fetchall()
    return name

def get_student_answers(student_id, test=False):
    """
    Return all answers associated with a student's id

    Args:
        student_id: A single student's id

    Returns:
        A list of answer db tuples
    """
    with dbconnect(test) as c:
        answers = c.execute(
            'SELECT * FROM answers WHERE student_id=? ORDER BY id DESC', 
            [student_id,],
        ).fetchall()
    return answers

def get_all_students(test=False):
    """
    Return all students' information

    Returns:
        A list of student db entries
    """
    with dbconnect(test) as c:
        students = c.execute('SELECT * FROM students').fetchall()
    return students

def get_all_student_IDs(test=False):
    """
    Return all students' information

    Returns:
        A list of all students' id numbers
    """
    with dbconnect(test) as c:
        students = c.execute('SELECT id FROM students').fetchall()
    return students

###########################################
#                Inserts                  #
###########################################

def insert_student_team_pairs(student_and_team_ids, test=False):
    """
    Insert list of student_id team_id pairs into database

    Args:
        student_and_team_ids: list of (student_id, team_id) pairs
    """
    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO assignments (student_id, team_id) VALUES (?,?)', 
            student_and_team_ids,
        )

def insert_students(students, test=False):
    """
    Insert list of new students into database

    Args: 
        students: list of (name, username) for each student
    """  
    if any(len(student) != 2 for student in students):
        raise ValueError('Insert expected name and username for every student.')
    current_time = datetime.datetime.now().isoformat()
    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO students (name, created_at, updated_at, username) VALUES (?, current_time, current_time, ?);', 
            students,
        )

def insert_answers(values, student_ids, questions, test=False):
    """
    Insert list of new answers into database

    Args:
        values: the values for each answer
        student_ids: student's id for each answer
        question: the question for each answer
    """
    length = len(values)
    if not all(length == len(lst) for lst in [values, student_ids, questions]):
        raise ValueError('Inputs are not the same length')
    answers = [[values[i], student_ids[i], questions[i]] for i in range(length)]
    current_time = datetime.datetime.now().isoformat()

    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO answers (value, created_at, updated_at, student_id, question) VALUES (?, current_time, current_time, ?, ?);', 
            answers,
        )

def insert_styles(styles, test=False):
    """
    Insert list of new styles into database

    Args: 
        styles: list of (student_id, communicator, collaborator, challenger, contributor)
    """
    if any(len(style) != 5 for style in styles):
        raise ValueError('Insert expected 5 inputs for every style.')
    current_time = datetime.datetime.now().isoformat()

    with dbconnect(test) as c:
        c.executemany(
            'INSERT INTO styles (student_id, communicator, collaborator, challenger, contributor, created_at, updated_at) VALUES (?, ?, ?, ?, ?, current_time, current_time);', 
            styles,
        )


###########################################
#                DELETE                   #
###########################################

def remove_all(test=False):
    """
    Remove all entries in database PERMANENTLY
    """
    with dbconnect(test) as c:
        c.execute('DELETE FROM students')
        c.execute('DELETE FROM styles')
        c.execute('DELETE FROM answers')
        
