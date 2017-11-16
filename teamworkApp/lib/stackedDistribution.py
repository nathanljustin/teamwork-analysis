# muddersOnRails()
# Maeve Murphy November 15, 2017
# Last updated: 11-15-17

# creates a histogram that shows the number of students with
# primary, secondary, tertiary, and quarternary rankings
# of each type.

# resources:
# https://matplotlib.org/examples/pylab_examples/bar_stacked.html

import matplotlib.pyplot as plt
import numpy as np
from enum import IntEnum
import sqlite3

DB = 'db/development.sqlite3'
Style = IntEnum('Style', 'Communicator, Collaborator, Challenger, Contributor', start=0)

def get_style_tuples():
    """Retrieve all the style data stored in the database"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        'SELECT communicator, collaborator, challenger, contributor FROM styles'
    )
    style_data = c.fetchall()
    conn.commit()
    conn.close()

    return style_data

def tally_nth(style_data, n):
    """given a tuple of 4 scores: (communicator, collaborator,
    challenger, contributor), return tallies for how many
    students in the DB have each as their nth order prominence of style.
    For example, let n = 1 and get back the highest order prominence (primary)
        style
    NOTE: ties are settled such that they are counted in both categories of the
    tie. For example, if the student's style was [45, 43, 43, 49] collaborator
    would be 2nd and 3rd and challenger would *also* be 2nd and 3rd"""
    # communicator, collaborator, challenger, contributor
    tallies = [0,0,0,0]
    for student in style_data:
        # sort from low to high
        sorted_styles = sorted(student)
        # max is -1, second greatest is -2, etc.
        if student[0] == sorted_styles[-n]:
            tallies[0] += 1
        if student[1] == sorted_styles[-n]:
            tallies[1] += 1
        if student[2] == sorted_styles[-n]:
            tallies[2] += 1
        if student[3] == sorted_styles[-n]:
            tallies[3] += 1
    return tallies


def make_stacked_graph(primaries, secondaries, tertiaries, quarternaries):
    """Given all the prominences of styles from the style table in the
        database, create a stacked graph to aggregate the information
        into one place by stacknig them in a histogram."""
    x_labels = [Style(x).name for x in range(len(Style))]

    # find the max height and scale the graph accordingly
    heights = [0,0,0,0]
    for i in range(0,4):
        heights[i] = primaries[i] + secondaries[i] + tertiaries[i] + quarternaries[i]
    max_y = max(heights)
    increment = 1
    # if the max is too big, split the ticks on the y axis for readablity
    if max_y >= 30:
        increment = 2

    N = 4
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars

    # stack each ranking
    # bottom is calculated such that it sits on top of rankings
    # of higher order
    prim  = plt.bar(ind, primaries, width, color='#82ccc4')
    sec   = plt.bar(ind, secondaries, width, color='#777ea8',
                  bottom=np.array(primaries))
    tert  = plt.bar(ind, tertiaries, width, color='#008081',
                  bottom=(np.array(secondaries) + np.array(primaries)))
    quart = plt.bar(ind, quarternaries, width, color='#c4d89e',
                  bottom=(np.array(secondaries)
                  + np.array(tertiaries) + np.array(primaries)))

    plt.ylabel('Number of Students')
    plt.title('Scores by Order of Styles')
    plt.xticks(ind, x_labels)
    plt.yticks(np.arange(0, max_y+2, increment))
    plt.legend((prim[0], sec[0], tert[0], quart[0]),
                    ('Primary', 'Secondary', 'Tertiary', 'Quaternary'))

    plt.show()

def main():
    tuples        = get_style_tuples()
    primaries     = tally_nth(tuples, 1)
    secondaries   = tally_nth(tuples, 2)
    tertiaries    = tally_nth(tuples, 3)
    quarternaries = tally_nth(tuples, 4)

    make_stacked_graph(primaries, secondaries, tertiaries, quarternaries)

if __name__ == "__main__":
	main()
