# muddersOnRails()
# Maeve Murphy October 12, 2017
# Last updated: 11-9-2017

# imports data from the .csv file holding responses from the teamwork survey

# resources:
# https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
# https://docs.python.org/2/library/sqlite3.html

import argparse
import sqlite3
import csv
from datetime import datetime, date, time

import dbCalls
from evaluateAnswers import *

EXPANDED_QUESTIONS = 72
TEST = False


def get_answer(answer_num):
    for ans in range(len(Answer_Value)):
        if Answer_Value(ans).name == answer_num:
            return ans
    raise ValueError("Invalid response")

def process_answer_data(csv_filename):
    """Given the Teamwork Survey csv file, process_answer_data will extract the
    pertinent information and populate a student dictionary with it.
    This processing requires very specifically formatted .csv files and it
    assumes they come from the results of the Teamwork Survey sent out by
    muddersOnRails.
    input csv_filename: name (and possibly path to) the csv file corresponding
        to the data received by respondants to the Teamwork Survey
    output student_dict: a dictionary. The keys are usernames of students
        collected from the Teamwork Survey. The value for each key is a list of
        three pieces of information:
            [timestamp, expanded_responses, enummed_responses]
            timestamp: the time at which the student filled out the Teamwork
                Survey.
            expanded_responses: the responses to each question expanded out into
                a string of the four-digit integer corresponding to their
                rankings, this is a list of 18 responses.
            enummed_responses: the list of responses to each question enumerated
                according to the IntEnum Answer_Value. This is a list of 18
                integers corresponding to the IntEnum."""
    with open(csv_filename) as csvfile:

        # the student dictionary has keys of student usernames and values
            # explained in the docstring
        student_dict       = {}

        # read the csv file
        answer_reader = csv.reader(csvfile)
        student_data  = list(answer_reader)
        # get rid of the row with questions
        student_data  = student_data[1:]

        for student in student_data:
            # these are the 18x4 responses to the survey
            teamwork_responses = student[1:EXPANDED_QUESTIONS+1]
            # expanded responses are of the form 'wxyz' where w != x != y != z
                # and w, x, y, and z are all values between 1 and 4 inclusive
            expanded_responses = []
            # enummed responses correspond to an integer between 0 and 23
                # inclusive where the integer is the value in Answer_Value
            enummed_responses  = []
            count = 0
            while (count < EXPANDED_QUESTIONS):
                # grab the next four digits and "glue" them together
                    # to creat the expanded response
                expanded_responses.append(
                                    teamwork_responses[count]   +
                                    teamwork_responses[count+1] +
                                    teamwork_responses[count+2] +
                                    teamwork_responses[count+3]
                                    )
                # increment by to not quadruple count characters
                count += 4
            # find the corresponding value to this expanded response
            for resp in expanded_responses:
                ans = get_answer(resp)
                enummed_responses.append(ans)

            # the timestamps are saved in the first column of the .csv file
            timestamp = student[0]
            student_dict[student[-1]] = [timestamp, expanded_responses, enummed_responses]

        return student_dict

def find_style(expanded_responses):
    #TODO: This is basically deprecated as we are going to use evaluateAnswers
        # for this calculation
    contributor  = 0
    collaborator = 0
    communicator = 0
    challenger   = 0
    tracker      = 0
    for resp in expanded_responses:
        # this pattern is based on the teamwork survey scoring scheme
        if tracker == 0:
            contributor  += int(resp[0]) # a
            collaborator += int(resp[1]) # b
            communicator += int(resp[2]) # c
            challenger   += int(resp[3]) # d
        elif tracker == 1:
            contributor  += int(resp[3]) # d
            collaborator += int(resp[0]) # a
            communicator += int(resp[1]) # b
            challenger   += int(resp[2]) # c
        elif tracker == 2:
            contributor  += int(resp[2]) # c
            collaborator += int(resp[3]) # d
            communicator += int(resp[0]) # a
            challenger   += int(resp[1]) # b
        elif tracker == 3:
            contributor  += int(resp[1]) # b
            collaborator += int(resp[2]) # c
            communicator += int(resp[3]) # d
            challenger   += int(resp[0]) # a
        else:
            tracker = -1
        tracker += 1
    return communicator, collaborator, challenger, contributor

def list_student_data(student_dict):
    """Using data from the csv file given, insertstudent_data finds how many
    students are in the file and places them into the student table"""
    student_to_db = []

    for student in student_dict.keys():
        now = datetime.now().isoformat()
        # TODO(Maeve): add functionality to get which team the student is on.
            # This will require more functionality on the teams side
        # currently name and username are the same
        student_to_db.append((student, student_dict[student][0], now, student))
    return student_to_db

def list_answer_data(student_dict):
    """Return the list of answer data corresponding to each student within
    student_dict.
    output: answer_to_db is a list of tuples holding information corresponding
        to the columns within the answers table that is inserted in a future
        function."""
    # fetch the names of the students from the table

    temp_keys = dbCalls.get_all_student_IDs(TEST)

    primary_keys  = [temp_key[0] for temp_key in temp_keys]
    answer_to_db = []
    count = 0

    # iterate through the students to find the enumerated responses to each
        # question along with student_id and relevant timestamps
    for student in student_dict.keys():
        now                  = datetime.now().isoformat()
        enummed_responses     = student_dict[student][2]
        question_count       = 0

        for response in enummed_responses:
            answer_to_db.append((
                response,
                student_dict[student][0],
                now,
                primary_keys[count],
                question_count
            ))
            question_count += 1
        count += 1
    return answer_to_db

def list_style_data(student_dict):
    """Given a dictionary of student data, calculate and import style data
    for each student.
    Uses find_style to calculate styles."""
    style_to_db = []

    temp_keys = dbCalls.get_all_student_IDs(TEST)

    primary_keys = [temp_key[0] for temp_key in temp_keys]

    count = 0
    for student in student_dict.keys():
        now               = datetime.now().isoformat()
        expanded_responses = student_dict[student][1]
        communicator, collaborator, challenger, contributor = find_style(expanded_responses)
        # TODO: The commented out line below should be what we use in the
            # future; however, evaluateAnswers has not been updated for the
            # new schema (as of the time of writing this 10-28-2017) so we
            # cannot use it yet
        # (communicator, collaborator, challenger, contributor) = find_scores(primary_keys[count])
        created_at   = student_dict[student][0]
        student_id   = primary_keys[count]
        style_to_db.append((
                student_id,
                communicator,
                collaborator,
                challenger,
                contributor,
                created_at,
                now
            ))
        count += 1

    return style_to_db

def execute_insert(csv_filename):
    student_dict   = process_answer_data(csv_filename)
    student_to_db = list_student_data(student_dict)
    print("Inserting .csv information into 'students'...")

    dbCalls.insert_students(student_to_db, TEST)

    print("Success.")
    # answer and style depend on information being stored in students so we
        # can only call list_answer_data and list_student_data after
        # list_student_data's information has been inserted
    answer_to_db  = list_answer_data(student_dict)
    style_to_db   = list_style_data(student_dict)
    print("Inserting data into 'answers' and 'styles'...")

    values = [item[0] for item in answer_to_db]
    student_ids = [item[3] for item in answer_to_db]
    questions = [item[4] for item in answer_to_db]
    dbCalls.insert_answers(values, student_ids, questions, TEST)
    dbCalls.insert_styles(style_to_db, TEST)

    print("Success: Data inserted into 3 tables!")

def check_inputs(filename, test=False):
    """Checks the inputs and then starts the import process"""
    if test: 
        global TEST # needed to modify global variable TEST
        TEST = True

    # TODO: remove this and other print statements when moving to Ruby
    print("Inserting data")

    # make sure the file is a csv
    if filename[-4:] == ".csv":
        # make sure the path has been properly specified
        try:
            execute_insert(filename)
        except FileNotFoundError:
            print("File must have an accessible path!")
    else:
        print("File must be a CSV with extension .csv!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import csv file")
    parser.add_argument(
        'filepath',  
        help='Path to file',
    )
    parser.add_argument(
        '-t', '--test', 
        dest='test',
        action='store_true',
        help='Student id for desired student graph',
    )
    args = parser.parse_args()

    check_inputs(args.filepath, args.test)
