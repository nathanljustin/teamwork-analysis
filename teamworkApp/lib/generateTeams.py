import random
import sqlite3
from enum import IntEnum

DB = 'db/development.sqlite3'

Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)
Answer_Value = IntEnum(
	'Answer_Value', 
	'1234 1243 1324 1342 1423 1432 2134 2143 2314 2341 2413 2431 3124 3142 3214 3241 3412 3421 4123 4132 4213 4231 4312 4321',
	start=0
)

def update_teams(team_size):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute('SELECT * FROM students')

	rows = c.fetchall()
	random.shuffle(rows)

	# find an integer number of teams based on team size
	number_of_teams = int(len(rows)/team_size)

	# create at least 1 team
	if number_of_teams == 0:
		number_of_teams += 1

	# update database entries based on random reordering
	for i, row in enumerate(rows):
		c.execute(
			"UPDATE students set team=? where id=?",
			[(i % number_of_teams), row[0]],
		)

	conn.commit()
	conn.close()

def main():
	team_size = 1
	update_teams(team_size)

if __name__ == "__main__":
	main()
