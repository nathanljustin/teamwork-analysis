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
    conn.commit()
    conn.close()
    
    # Get the scores needed
    assert(len(dbData) != 0), "Cannot find student data."
    scores = dbData[0][2:6]

    # Make graph
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))
    plt.bar(yPos, scores, align = 'center', alpha = 0.5)
    plt.xticks(yPos, labels)
    plt.ylabel("Score")
    plt.title("Student " + str(student_id) + " Distribution of Types")

    # Make graph
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))

    plt.bar(yPos, scores, align = 'center', alpha = 0.5)
    plt.xticks(yPos, labels)
    plt.ylabel("Score")
    plt.title("Student " + str(student_id) + " Distribution of Types")

    name = 'app/assets/images/summary' + str(student_id) + '.png'
    plt.savefig(name, bbox_inches='tight')

if __name__ == "__main__":
    student_graph(1)
    