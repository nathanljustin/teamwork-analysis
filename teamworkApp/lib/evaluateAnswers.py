from enum import IntEnum
import sqlite3

DB = 'db/development.sqlite3'

NUM_QUESTIONS = 18

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

def get_students_answers(student_ids):
    """return list of complete answers for a given student"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = []
    for i in range(len(student_ids)):
        c.execute(
            'SELECT * FROM answers WHERE student_id=?',
            [student_ids[i],],
        )
        rows += [(c.fetchall())]

    conn.commit()
    conn.close()
    return rows

def find_scores(student_ids):
    """Returns a student's scores for each of the possible styles in a tuple"""
    all_scores = []
    responses = []
    student_responses = []
    questions = range(NUM_QUESTIONS)
    answer_rows = get_students_answers(student_ids)
    for row in answer_rows:
        responses = [Answer_Value(ans[1]).name for ans in row]
        student_responses.append(responses)
    scores = [0] * len(Style)
    for resp in student_responses:
        scores = [0] * len(Style)
        for question in questions:
            order = Questions[question % 4]
            for i, style in enumerate(order):
                scores[style.value] += int(resp[question][i])
        all_scores.append(tuple(scores))
    return all_scores
