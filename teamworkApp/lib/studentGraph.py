from enum import IntEnum
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

DB = 'db/development.sqlite3'

Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)
Answer_Value = IntEnum(
    'Answer_Value', 
    '1234 1243 1324 1342 1423 1432 2134 2143 2314 2341 2413 2431 3124 3142 3214 3241 3412 3421 4123 4132 4213 4231 4312 4321',
    start=0
)


# the order of answers repeat every 4 questions so just the index is (question_num % 4) 
Questions = {
    0: (Style.Contributor, Style.Collaborator, Style.Communicator, Style.Challenger),
    1: (Style.Collaborator, Style.Communicator, Style.Challenger, Style.Contributor),
    2: (Style.Communicator, Style.Challenger, Style.Contributor, Style.Collaborator),
    3: (Style.Challenger, Style.Contributor, Style.Collaborator, Style.Communicator),
}

def get_students_answers(student_id):
    """return list of complete answers for a given student"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        'SELECT * FROM answers WHERE student_id=?', 
        [student_id,],
    )
    rows = c.fetchall()

    conn.commit()
    conn.close()

    return rows

def find_scores(student_id):
    """Returns a student's scores for each of the possible styles in a tuple"""
    answers = get_students_answers(student_id)
    questions = [answer[5] for answer in answers]
    values = [Answer_Value(answer[1]).name for answer in answers]
    scores = [0] * len(Style)
    
    for question in range(len(questions)):
        order = Questions[question % 4]
        for i, style in enumerate(order):
            scores[style.value] += int(values[question][i])

    return tuple(scores)

def student_graph(student_id):
    """Returns a path to where the student's graph is saved"""

    labels = [Style(x).name for x in range(len(Style))]
    scores = find_scores(student_id)

    fig1, ax1 = plt.subplots()
    ax1.pie(scores, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    plt.show()

if __name__ == "__main__":
    student_graph(1)

