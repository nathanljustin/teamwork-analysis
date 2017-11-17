from enum import IntEnum

import dbCalls

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

def find_scores(student_id):
    """Returns a student's scores for each of the possible styles in a tuple"""
    answers = dbCalls.get_student_answers(student_id)
    questions = [answer[5] for answer in answers]
    values = [Answer_Value(answer[1]).name for answer in answers]
    scores = [0] * len(Style)
    
    for question in range(len(questions)):
        order = Questions[question % 4]
        for i, style in enumerate(order):
            scores[style.value] += int(values[question][i])

    return tuple(scores)