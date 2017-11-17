# muddersOnRails()
# Maeve Murphy November 15, 2017
# Last updated: 11-16-17

# creates a histogram that shows the number of students with
# primary, secondary, tertiary, and quarternary rankings
# of each type.

# resources:
# https://matplotlib.org/examples/pylab_examples/bar_stacked.html

import matplotlib.pyplot as plt
import numpy as np
from evaluateAnswers import Style
from dbCalls import *
import sqlite3


def get_style_tuples():
    """Retrieve all the style data stored in the database"""
    style_info = get_all_styles()
    style_data = [i[2:6] for i in style_info]

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
        indexes = [i for i, x in enumerate(student) if x == sorted_styles[-n]]
        for i in indexes:
            tallies[i] += 1
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
        max_y += 3

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
                    ('Primary', 'Secondary', 'Tertiary', 'Quaternary'), bbox_to_anchor=(1.05, 1), loc=2,borderaxespad=0.)

    plt.savefig('app/assets/images/overall.png', bbox_inches='tight')

def main():
    tuples        = get_style_tuples()
    primaries     = tally_nth(tuples, 1)
    secondaries   = tally_nth(tuples, 2)
    tertiaries    = tally_nth(tuples, 3)
    quarternaries = tally_nth(tuples, 4)

    make_stacked_graph(primaries, secondaries, tertiaries, quarternaries)

if __name__ == "__main__":
	main()
