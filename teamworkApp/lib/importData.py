import sqlite3

DB = 'db/development.sqlite3'

def main():

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	for row in c.execute('SELECT * FROM students'):
		print(row)

	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
