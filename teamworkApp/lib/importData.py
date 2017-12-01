# muddersOnRails()
# Maeve Murphy October 12, 2017
# Last updated: 11-14-2017

# imports data from the .csv file holding responses from the teamwork survey

# resources:
# https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
# https://docs.python.org/2/library/sqlite3.html

import argparse
import sqlite3
import csv

from dbCalls import *
from evaluateAnswers import *

EXPANDED_QUESTIONS = 72
USERNAME_COL = 80
TEST = False


def get_answer(answer_num):
    """
    Given answer number find appropriate response according to Answer_Value
    """
    for ans in range(len(Answer_Value)):
        if Answer_Value(ans).name == answer_num:
            return ans
    raise ValueError("Invalid response")

def process_answer_data(csv_filename):
    """
    Process data from temawork survey .csv

    Given the Teamwork Survey csv file, process_answer_data will extract the
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
            student_dict[student[USERNAME_COL]] = [timestamp, expanded_responses, enummed_responses]

        return student_dict


def list_student_data(student_dict):
    """
    Create list of student_ids to go in student table

    Using data from the csv file given, insertstudent_data finds how many
    students are in the file and creates a list to enter them into
    the student table
    inputs: student_dicts from process_answer_data
    output: list of student info to go in students (ids)
    """
    student_to_db = []
    for student in student_dict.keys():
        # TODO(Future work): add functionality to get which team the student is on.
            # This will require more functionality on the teams side
        # currently name and username are the same
        student_to_db.append((student, student))
    return student_to_db

def list_answer_data(student_dict):
    """
    Return the list of answer data corresponding to each student in student_dict

    output: answer_to_db is a list of tuples holding information corresponding
        to the columns within the answers table that is inserted in a future
        function.
    """
    # fetch the names of the students from the table

    temp_keys = dbCalls.get_all_student_IDs(TEST)

    primary_keys  = [temp_key[0] for temp_key in temp_keys]
    answer_to_db = []
    count = 0

    # iterate through the students to find the enumerated responses to each
        # question along with student_id and relevant timestamps
    for student in student_dict.keys():
        enummed_responses     = student_dict[student][2]
        question_count       = 0

        for response in enummed_responses:
            answer_to_db.append((
                response,
                student_dict[student][0],
                primary_keys[count],
                question_count
            ))
            question_count += 1
        count += 1
    return answer_to_db

def list_style_data(student_dict):
	"""
    Find student styles and format them into a list for the database

    Given a dictionary of student data, calculate and import style data
	for each student. Uses find_style to calculate styles.
    """
	style_to_db = []
	# fetch the names of the students from the table
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# get the primary keys for the students
	c.execute('SELECT id FROM students;')
	temp_keys = c.fetchall()
	conn.commit()
	conn.close()

	primary_keys = [temp_key[0] for temp_key in temp_keys]

	count = 0
	for student in student_dict.keys():
		expanded_responses = student_dict[student][1]
		# call find_scores from evaluateAnswers
		(contributor, collaborator, communicator, challenger) = find_scores(expanded_responses)
		# created_at   = student_dict[student][0]
		student_id   = primary_keys[count]
		style_to_db.append((
				student_id,
                communicator,
				collaborator,
				challenger,
                contributor
			))
		count += 1

	return style_to_db

def execute_insert(csv_filename):
    """
    Given csv file perform all functions to process data for the database.

    These functions are process_answer_data, list_student_data, list_answer_data,
    and list_style_data. The lists are then all inserted into the database.
    """
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
    # print("answer is ", answer_to_db)
    values = [item[0] for item in answer_to_db]
    student_ids = [item[2] for item in answer_to_db]
    questions = [item[3] for item in answer_to_db]
    dbCalls.insert_answers(values, student_ids, questions, TEST)
    dbCalls.insert_styles(style_to_db, TEST)

    print("Success: Data inserted into 3 tables!")

def check_inputs(filename, test=False):
    """ Checks the inputs and then starts the import process """
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
        except FileNotFoundError as error:
            print("File must have an accessible path!")
            raise error
    else:
        print("File must be a CSV with extension .csv!")
        raise ValueError("Needs a CSV input")

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
