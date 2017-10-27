# muddersOnRails()
# Maeve Murphy October 12, 2017
# Last updated: 10-27-2017

# imports data from the .csv file holding responses from the teamwork survey

# resources:
# https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
# https://docs.python.org/2/library/sqlite3.html

import sqlite3
import csv
from datetime import datetime, date, time
from enum import IntEnum

DB = 'db/development.sqlite3'
Answer_Value = IntEnum(
	'Answer_Value',
	'1234 1243 1324 1342 1423 1432 2134 2143 2314 2341 2413 2431 3124 3142 3214 3241 3412 3421 4123 4132 4213 4231 4312 4321',
	start=0
)

def getAnswer(answerNum):
	for ans in range(0, 23):
		if Answer_Value(ans).name == answerNum:
			return ans
	raise ValueError("Invalid response")

def processAnswerData(csvFileName):
	"""Given the Teamwork Survey csv file, processAnswerData will extract the
	pertinent information and populate a student dictionary with it.
	This processing requires very specifically formatted .csv files and it
	assumes they come from the results of the Teamwork Survey sent out by
	muddersOnRails.
	input csvFilename: name (and possibly path to) the csv file corresponding
		to the data received by respondants to the Teamwork Survey
	output studentDict: a dictionary. The keys are usernames of students
		collected from the Teamwork Survey. The value for each key is a list of
		three pieces of information:
			[timestamp, expandedResponses, enummedResponses]
			timestamp: the time at which the student filled out the Teamwork
				Survey.
			expandedResponses: the responses to each question expanded out into
				a string of the four-digit integer corresponding to their
				rankings, this is a list of 18 responses.
			enummedResponses: the list of responses to each question enumerated
				according to the IntEnum Answer_Value. This is a list of 18
				integers corresponding to the IntEnum."""
	with open(csvFileName) as csvfile:

		timestamps        = []
		expandedResponses = []
		studentDict       = {}

		answerReader = csv.reader(csvfile)
		studentData  = list(answerReader)
		# get rid of the row with questions
		studentData  = studentData[1:]

		for student in studentData:
			# these are the 18x4 responses to the survey
			teamworkResponses = student[1:73]
			expandedResponses = []
			enummedResponses  = []
			count = 0
			while (count < 72):
				expandedResponses += [ teamworkResponses[count]   +
								       teamworkResponses[count+1] +
								       teamworkResponses[count+2] +
								       teamworkResponses[count+3] ]
				count += 4
			for resp in expandedResponses:
				ans = getAnswer(resp)
				enummedResponses += [ans]

			# the timestamps are saved in the first column of the .csv file
			timestamp = student[0]
			studentDict[student[-1]] = [timestamp, expandedResponses, enummedResponses]

		return studentDict

def findStyle(expandedResponses):
	contributor  = 0
	collaborator = 0
	communicator = 0
	challenger   = 0
	tracker      = 0
	for resp in expandedResponses:
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

def listStudentData(studentDict):
	"""Using data from the csv file given, insertStudentData finds how many
	students are in the file and places them into the student table"""
	student_to_db = []

	for student in studentDict.keys():
		now = datetime.now().isoformat()
		# TODO(Maeve): add functionality to get which team the student is on.
			# This will require more functionality on the teams side
		# currently name and username are the same
		student_to_db += [(student, studentDict[student][0], now, student)]
	return student_to_db

def listAnswerData(studentDict):
	"""Import data from the csv file into answers and students
	within out SQLite3 database.
	csvFileName: name (possibly including path) of the
		with the desired data"""
	# fetch the names of the students from the table
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# get the primary keys for the students
	c.execute('SELECT id FROM students;')
	tempKeys = c.fetchall()
	conn.commit()
	conn.close()
	primaryKeys  = [tempKey[0] for tempKey in tempKeys]
	answer_to_db = []
	count = 0

	for student in studentDict.keys():
		now           = datetime.now().isoformat()
		responses     = studentDict[student][2]
		questionCount = 0

		for response in responses:
			answer_to_db += [
			(response,
			studentDict[student][0],
			now,
			primaryKeys[count],
			questionCount)
			]
			questionCount += 1
		count += 1
	return answer_to_db

def listStyleData(studentDict):
	"""Given a dictionary of student data, calculate and import style data
	for each student.
	Uses findStyle to calculate styles."""
	style_to_db = []
	# fetch the names of the students from the table
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# get the primary keys for the students
	c.execute('SELECT id FROM students;')
	tempKeys = c.fetchall()
	conn.commit()
	conn.close()

	primaryKeys = [tempKey[0] for tempKey in tempKeys]

	count = 0
	for student in studentDict.keys():
		now               = datetime.now().isoformat()
		expandedResponses = studentDict[student][1]
		communicator, collaborator, challenger, contributor = findStyle(expandedResponses)
		created_at   = studentDict[student][0]
		student_id   = primaryKeys[count]
		style_to_db += [
			(student_id,
			communicator,
			collaborator,
			challenger,
			contributor,
			created_at,
			now)
			]
		count += 1

	return style_to_db

def executeInsert(csvFileName):
	studentDict   = processAnswerData(csvFileName)
	student_to_db = listStudentData(studentDict)
	print("Inserting .csv information into 'students'...")
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# insert student data from .csv into students
	c.executemany('INSERT INTO students (name, created_at, updated_at, username) VALUES (?, ?, ?, ?);', student_to_db)
	conn.commit()
	conn.close()
	print("Success.")
	# answer and style depend on information being stored in students so we
		# can only call listAnswerData and listStudentData after
		# listStudentData's information has been inserted
	answer_to_db  = listAnswerData(studentDict)
	style_to_db   = listStyleData(studentDict)
	print("Inserting data into 'answers' and 'styles'...")

	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# insert answer data for each question for the student
	c.executemany('INSERT INTO answers (value, created_at, updated_at, student_id, question) VALUES (?, ?, ?, ?, ?);', answer_to_db)
	# insert style data for each student
	c.executemany('INSERT INTO styles (student_id, communicator, collaborator, challenger, contributor, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?);', style_to_db)
	conn.commit()
	conn.close()

	print("Success.")

def main():

	print("Inserting data")
	executeInsert('lib/test_spreadsheet.csv')
	print("Success: Data inserted into 3 tables!")

if __name__ == "__main__":
	main()
