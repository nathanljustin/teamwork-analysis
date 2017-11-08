from enum import IntEnum
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from findType import getType

DB = 'db/development.sqlite3'
Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)

def getStylesData():
    """Returns number of students per style"""

    # Get all scores
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    scores = c.execute('SELECT * FROM styles').fetchall()
    conn.commit()
    conn.close()

    # Get types from scores
    # If multiple types, all counted
    data = [0.0] * len(Style)

    # Loop through each student, and get the types of each student
    for i in range(len(scores)):
        studentScores = scores[i][2:6]
        types = getType(studentScores)
        length = len(types)
        for j in range(len(types)):
            data[types[j]] += 1.0/length
    
    return data

def main():
    """Gives the graph of the overall distribution of types"""
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))
    data = getStylesData()

    plt.bar(yPos, data, align = 'center', alpha = 0.5)
    plt.xticks(yPos, labels)
    plt.ylabel("Number of Students")
    plt.title("Overall Distribution of Types")

    plt.savefig('app/assets/images/overall.png', bbox_inches='tight')

if __name__ == "__main__":
    main()

    
