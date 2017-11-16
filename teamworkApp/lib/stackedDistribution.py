# muddersOnRails()
# Maeve Murphy November 15, 2017
# Last updated: 11-15-17

# creates a histogram that shows the number of students with
# primary, secondary, tertiary, and quarternary rankings
# of each type.

# resources:
# https://matplotlib.org/examples/statistics/histogram_demo_multihist.html

import matplotlib.pyplot as plt
import numpy as np
from enum import IntEnum
import sqlite3

DB = 'db/development.sqlite3'
Style = IntEnum('Style', 'Communicator, Collaborator, Challenger, Contributor', start=0)

def get_style_tuples():
    """Returns a path to where the student's graph is saved"""



    # Connect to db to get scores
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute(
        'SELECT communicator, collaborator, challenger, contributor FROM styles'
    )
    style_data = c.fetchall()
    conn.commit()
    conn.close()

    return style_data

def tally_primary(style_data):
    """given a tuple of 4 scores: (communicator, collaborator,
    challenger, contributor), return tallies for how many
    students in the DB have each as their primary"""
    # communicator, collaborator, challenger, contributor
    tallies = [0,0,0,0]
    for student in style_data:
        if student[0] == max(student):
            tallies[0] += 1
        elif student[1] == max(student):
            tallies[1] += 1
        elif student[2] == max(student):
            tallies[2] += 1
        else:
            tallies[3] += 1
    return tallies

def tally_secondary(style_data):
    # communicator, collaborator, challenger, contributor
    tallies = [0,0,0,0]
    for student in style_data:
        sorted_styles = sorted(student)
        if student[0] == sorted_styles[-2]:
            tallies[0] += 1
        if student[1] == sorted_styles[-2]:
            tallies[1] += 1
        if student[2] == sorted_styles[-2]:
            tallies[2] += 1
        if student[3] == sorted_styles[-2]:
            tallies[3] += 1
    return tallies

def tally_tertiary(style_data):
    # communicator, collaborator, challenger, contributor
    tallies = [0,0,0,0]
    for student in style_data:
        sorted_styles = sorted(student)
        if student[0] == sorted_styles[-3]:
            tallies[0] += 1
        if student[1] == sorted_styles[-3]:
            tallies[1] += 1
        if student[2] == sorted_styles[-3]:
            tallies[2] += 1
        if student[3] == sorted_styles[-3]:
            tallies[3] += 1
    return tallies

def tally_quaternary(style_data):
    # communicator, collaborator, challenger, contributor
    tallies = [0,0,0,0]
    for student in style_data:
        sorted_styles = sorted(student)
        if student[0] == sorted_styles[0]:
            tallies[0] += 1
        if student[1] == sorted_styles[0]:
            tallies[1] += 1
        if student[2] == sorted_styles[0]:
            tallies[2] += 1
        if student[3] == sorted_styles[0]:
            tallies[3] += 1
    return tallies

def make_stacked_graph(primaries, secondaries, tertiaries, quarternaries):
    """graphs yay"""
    # x_labels = [Style(x).name for x in range(len(Style))]
    #
    # n_bins = 4
    # x = primaries, secondaries
    # yPos = np.arange(len(x_labels))
    #
    # print(primaries)
    #
    # # fig, ax1 = plt.subplots(nrows=1, ncols=1)
    # # ax1 = axes.flatten()
    #
    # # colors =  ['#3fe0d0', '#111e6c', '#008081', '#a3de38']
    # # ax0.hist(x, n_bins, normed=1, histtype='bar', color=colors, label=colors)
    # # ax0.legend(prop={'size': 10})
    # # ax0.set_title('bars with legend')
    #
    # # plt.hist(x, n_bins, histtype='barstacked')#, color=colors)
    # # plt.set_title('stacked bar')
    # plt.hist(yPos, x, histtype='barstacked', align = 'center', alpha = 0.5)
    # plt.xticks(yPos, x_labels)
    # plt.ylabel("Score")
    # plt.title("Student")
    #
    #
    # # fig.tight_layout()
    # plt.show()


    N = 4
    menMeans = (20, 35, 30, 35, 27)
    womenMeans = (25, 32, 34, 20, 25)
    menStd = (2, 3, 4, 1, 2)
    womenStd = (3, 5, 2, 3, 3)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, primaries, width, color='#d62728')
    p2 = plt.bar(ind, secondaries, width,
                 bottom=primaries)
    p2 = plt.bar(ind, tertiaries, width,
                  bottom=secondaries)
    p2 = plt.bar(ind, quarternaries, width,
               bottom=tertiaries)

    plt.ylabel('Scores')
    plt.title('Scores by group and gender')
    plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
    plt.yticks(np.arange(0, 25, 10))
    plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    plt.show()

def main():
    tuples        = get_style_tuples()
    primaries     = tally_primary(tuples)
    secondaries   = tally_secondary(tuples)
    tertiaries    = tally_tertiary(tuples)
    quarternaries = tally_quaternary(tuples)

    make_stacked_graph(primaries, secondaries, tertiaries, quarternaries)

if __name__ == "__main__":
	main()
