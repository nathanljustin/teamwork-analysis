import sqlite3
import csv
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
	"""Given the number of students and a csv file, importAnswerData will
	obtain the answers for the number of students given for 18 questions
	and return it as a dictionary the size of the number of students with 18
	responses.  Each response is originally comprised of 4 parts but is
	summarized into one of the 24 possible responses."""
	processedData = {}
	with open(csvFileName) as csvfile:
		answerReader = csv.reader(csvfile)
		studentData = list(answerReader)
		studentData = studentData[1:]
		timestamps = []
		studentResponses = []
		for student in studentData:
			timestamps += student[0]
			teamworkResponses = student[1:73]
			listOfStrings = []
			enummedResponses = []
			count = 0
			while (count < 72):
				listOfStrings += [teamworkResponses[count] +
								 teamworkResponses[count+1] +
								 teamworkResponses[count+2] +
								 teamworkResponses[count+3]]
				count += 4
			for resp in listOfStrings:
				ans = getAnswer(resp)
				enummedResponses += [ans]
			studentResponses.append(enummedResponses)
		return timestamps, studentResponses

def insertAnswerData(csvFileName):
	"""Import data from the csv file into the specified
	table within out SQLite3 database.
	csvFileName: name (possibly including path) of the
		with the desired data
	tableName: table where data is to be stored
	col1: starting column
	col2: ending column"""
# THIS WORKS SO REFINE THIS
	timestamps, studentResponses = processAnswerData(csvFileName)
	count = 0
	for students in studentResponses:
		studentId = 'S' + str(count)
		for response in students:
			to_db = [response, timestamps[count], timestamps[count], studentId, count]
			conn = sqlite3.connect(DB)
			c = conn.cursor()
			c.execute('INSERT INTO answers (value, created_at, updated_at, student_id, question) VALUES (?, ?, ?, ?, ?);', to_db)
			conn.commit()
			conn.close()
			count += 1

# generate a bunch of data and shove it into answers
def main():

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	c.execute('SELECT * FROM students;')
	# insertAnswerData('lib/test_spreadsheet.csv')
	# c.execute('SELECT * FROM answers;')

	print(c.fetchone())

	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
