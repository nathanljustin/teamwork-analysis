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
    contributor = c.execute('SELECT contributor FROM styles').fetchall()
    collaborator = c.execute('SELECT collaborator FROM styles').fetchall()
    communicator = c.execute('SELECT communicator FROM styles').fetchall()
    challenger = c.execute('SELECT challenger FROM styles').fetchall()
    conn.commit()
    conn.close()

    # Get types from scores
    # If multiple types, all counted
    data = [10] * len(Style)

    for i in range(len(contributor)):
        studentScores = [contributor[i], collaborator[i], communicator[i], challenger[i]]
        types = getType(studentScores)
        for j in range(len(types)):
            data[j] += 1
    
    return data

if __name__ == "__main__":
    """Gives the graph of the overall distribution of types"""
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))
    data = getStylesData()

    plt.bar(yPos, data, align = 'center', alpha = 0.5)
    plt.xticks(yPos, labels)
    plt.ylabel("Number of Students")
    plt.title("Overall Distribution of Types")

    plt.savefig('tmp/overall.png', bbox_inches='tight')
    