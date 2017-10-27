# resources:

# muddersOnRails()
# Maeve Murphy October 12, 2017
# Last updated: 10-20-2017

# imports data from the .csv file holding responses from the teamwork survey

import sqlite3
import csv
from datetime import datetime, date, time
from enum import IntEnum

DB = 'db/development.sqlite3'

Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)
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
	"""Given a csv file, importAnswerData will
	obtain the answers for the number of students given for 18 questions
	and return it as a dictionary the size of the number of students with 18
	responses.  Each response is originally comprised of 4 parts but is
	summarized into one of the 24 possible responses."""
	with open(csvFileName) as csvfile:

		timestamps = []
		expandedResponses = []
		studentResponses = []

		answerReader = csv.reader(csvfile)

		studentData = list(answerReader)
		studentData = studentData[1:]

		for student in studentData:
			# these are the 18x4 responses to the survey
			teamworkResponses = student[1:73]
			# the timestamps are saved in the first column
			timestamps += [student[0]]
			aggregateResponses = []
			enummedResponses = []
			count = 0
			while (count < 72):
				aggregateResponses += [teamworkResponses[count]   +
								       teamworkResponses[count+1] +
								       teamworkResponses[count+2] +
								       teamworkResponses[count+3]]
				count += 4
			expandedResponses += [aggregateResponses]

			for resp in aggregateResponses:
				ans = getAnswer(resp)
				enummedResponses += [ans]
			studentResponses.append(enummedResponses)

		return expandedResponses, timestamps, studentResponses

def findStyle(expandedResponses):
	contributor = 0
	collaborator = 0
	communicator = 0
	challenger = 0
	tracker = 0
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
	# currently does not account for having multiple dominant styles...
	if contributor == max(contributor, collaborator, communicator, challenger):
		return Style(0).name
	elif collaborator == max(contributor, collaborator, communicator, challenger):
		return Style(1).name
	elif communicator == max(contributor, collaborator, communicator, challenger):
		return Style(2).name
	else:
		return Style(3).name

def insertStudentData(csvFileName):
	"""Using data from the csv file given, insertStudentData finds how many
	students are in the file and places them into the student table"""

	expandedResponses, timestamps, studentResponses = processAnswerData(csvFileName)
	student_to_db = []
	count = 0

	for students in studentResponses:
		studentId = 'S' + str(count)
		now = datetime.now().isoformat()
		student_to_db += [(findStyle(expandedResponses[count]), studentId, 0, timestamps[count], now)]
		count += 1


	print("Inserting data into 'students'")
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# insert student data for each student
	c.executemany('INSERT INTO students (style, name, team, created_at, updated_at) VALUES (?, ?, ?, ?, ?);', student_to_db)
	conn.commit()
	conn.close()

def insertAnswerData(csvFileName):
	"""Import data from the csv file into answers and students
	within out SQLite3 database.
	csvFileName: name (possibly including path) of the
		with the desired data"""

	# fetch the names of the students from the table
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute('SELECT name FROM students;')
	names = c.fetchall()
	conn.commit()
	conn.close()

	students = []
	for name in names:
		students += [name[0]]

	expandedResponses, timestamps, studentResponses = processAnswerData(csvFileName)
	to_db = []
	# student_to_db = []
	count = 0

	for stdnt in studentResponses:
		questionCount = 0

		for response in stdnt:
			to_db += [(response, timestamps[count], timestamps[count], questionCount)]
			questionCount += 1

		now = datetime.now().isoformat()
		count += 1

	print("Inserting data into 'answers'")

	conn = sqlite3.connect(DB)
	c = conn.cursor()
	# insert student data for each question for the student
	c.executemany('INSERT INTO answers (value, created_at, updated_at,question) VALUES (?, ?, ?, ?);', to_db)
	conn.commit()
	conn.close()

def main():

	print("Inserting data")
	insertStudentData('lib/test_spreadsheet.csv')
	insertAnswerData('lib/test_spreadsheet.csv')
	print("Success: Data inserted into tables!")

if __name__ == "__main__":
	main()
