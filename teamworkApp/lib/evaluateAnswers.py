from enum import IntEnum
import sqlite3

DB = 'db/development.sqlite3'

QUESTIONS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

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


def find_scores(expanded_responses):
    """Given a list of expanded responses (i.e. '1234', '3214'...), find_scores
        will follow the scoring pattern outlined in Glenn Parker's
        teamwork survey.
        output: a tuple of four scores reflecting the four styles of the
            teamwork survey, ie
            (Contributor, Collaborator, Communicator, Challenger)"""
    scores = [0] * len(Style)
    # loop through all the numbers corresponding to questions
    for question in range(len(QUESTIONS)):
        #find the order in which to score the expanded response
        order = Questions[question % 4]
        for i, style in enumerate(order):
            # find the style and add it to the ongoing incrementation
            # of the score
            scores[style.value] += int(expanded_responses[question][i])
    #(contributor, collaborator, communicator, challenger)
    return tuple(scores)
