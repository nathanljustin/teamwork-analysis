import sqlite3
from enum import IntEnum

DB = 'db/development.sqlite3'

Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)
Answer_Value = IntEnum(
	'Answer_Value', 
	'1234 1243 1324 1342 1423 1432 2134 2143 2314 2341 2413 2431 3124 3142 3214 3241 3412 3421 4123 4132 4213 4231 4312 4321',
	start=0
)

def main():

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	c.execute('SELECT * FROM students')

	print(c.fetchone())

	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
