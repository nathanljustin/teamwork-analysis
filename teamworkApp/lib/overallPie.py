from enum import IntEnum
import sqlite3
import matplotlib.pyplot as plt

DB = 'db/development.sqlite3'
Style = IntEnum('Style', 'Contributor, Collaborator, Communicator, Challenger', start=0)

def getStylesData():
    """Returns number of students per style"""

    # Get all students
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    styles = c.execute('SELECT style FROM students').fetchall()
    conn.commit()
    conn.close()

    # Get number of students per style
    data = [0] * len(Style)
    for style in styles:
        data[style[0]] += 1
    
    return data

if __name__ == "__main__":
    """Gives the graph of the overall distribution of types"""
    labels = [Style(x).name for x in range(len(Style))]
    data = getStylesData()

    # In case no one has a certain style, don't put that style on the graph
    for i in range(len(data)-1, -1, -1):
        if data[i] == 0:
            del data[i]
            del labels[i]

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    plt.savefig('tmp/overall.png', bbox_inches='tight')
    