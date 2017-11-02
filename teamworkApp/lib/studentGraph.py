import argparse 
import matplotlib.pyplot as plt
import numpy as np
from enum import IntEnum
import sqlite3

DB = 'db/development.sqlite3'
Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)

def student_graph(student_id):
    """Returns a path to where the student's graph is saved"""

    labels = [Style(x).name for x in range(len(Style))]

    # Connect to db to get scores
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        'SELECT * FROM styles WHERE student_id=?', 
        [student_id,],
    )

    dbData = c.fetchall()

    scores = [0] * 4 
    if len(dbData) == 0:
        print("Error: Could not find any data on this student")
    else:
        scores = dbData[0][2:6]
    
    conn.commit()
    conn.close()

    # Make graph
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))

    plt.bar(yPos, scores, align = 'center', alpha = 0.5)
    plt.xticks(yPos, labels)
    plt.ylabel("Score")
    plt.title("Student " + str(student_id) + " Distribution of Types")

    name = 'tmp/summary' + str(student_id) + '.png'
    plt.savefig(name, bbox_inches='tight')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate graph summarizing a student's answers")
    parser.add_argument(
        'student_id', 
        type=int, 
        help='Student id for desired student graph',
    )
    args = parser.parse_args()

    student_graph(args.student_id)

