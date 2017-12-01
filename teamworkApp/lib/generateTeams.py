# muddersOnRails()
#
# Last updated:
# Collaborators:
#
# Overview:
#
# resources:

import argparse
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

def update_teams(args):
    """
    Given a team_size and number_of teams, randomly generate teams of students

    Edits the database to contain teams according to the number specified in
    the command line arguments, either number of teams and team size
    """

    # seperate arguments
    team_size = args.team_size
    number_of_teams = args.number_of_teams

    # create connection and find students
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM students')

    # randomize rows
    rows = c.fetchall()
    random.shuffle(rows)

    if team_size:
        number_of_teams = int(len(rows)/team_size)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate teams for the already inputed students')
    parser.add_argument(
        '--team-size',
        type=int,
        help='Desired size for each team, creates larger teams if not an even division',
        dest='team_size',
    )
    parser.add_argument(
        '--number-of-teams',
        type=int,
        help='Desired number of teams',
        dest='number_of_teams',
    )
    args = parser.parse_args()

    if not args.number_of_teams and not args.team_size:
        raise ValueError('No input for number of teams given.')
    update_teams(args)
