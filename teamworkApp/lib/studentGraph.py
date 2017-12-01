# muddersOnRails()
#
#

# creates a histogram that shows the scores for each style of the student
# selected on the webpage. Up to 6 students can be selected with all of their
# information individualized, but beyond six, only the average is shown because
# of the cluttered nature of the graph

# resources:
# https://matplotlib.org/examples/pylab_examples/bar_stacked.html
# https://chrisalbon.com/python/matplotlib_grouped_bar_plot.html

import argparse
import matplotlib.pyplot as plt
import numpy as np
import sys

import dbCalls
from evaluateAnswers import Style


def student_graph(student_ids):
    """
    Returns a path to where the student's generated graph is saved

    Given the student_ids, create a grouped bar graph of the students' scores
    and return the path to that .png to be displayed on the webpage.
    """

    labels = [Style(x).name for x in range(len(Style))]
    names = dbCalls.get_names(student_ids)
    # Connect to db to get scores
    dbData = dbCalls.get_students_styles(student_ids)
    yPos = np.arange(len(labels))
    scoreSet = [data[2:6] for data in dbData]

    # Get the scores needed
    assert(len(dbData) != 0), "Cannot find student data."

    # create split bar graph if <= 6 students
    if len(scoreSet) <= 6:
        # change for each set of bars
        widthChange = -0.4
        width = 0.8/len(scoreSet)
        colors = ['#3fe0d0', '#111e6c', '#008081', '#a3de38', '#3378e8', '#8733e8']
        currIter = 0
        for scores in scoreSet:
            username = names[currIter][0]
            plt.bar(yPos + widthChange, scores, width = width, color = colors[currIter],  align='edge', alpha = 0.5, label = username)
            widthChange += width
            currIter += 1

    # create summary graph if > 6 students
    else:
        # find avg val for each score
        avgScores = [float(sum(col))/len(col) for col in zip(*scoreSet)]
        plt.bar(yPos, avgScores, align = 'center', color='#3fe0d0', alpha = 0.5, label = 'Average Values')

    # Make graph
    plt.xticks(yPos, labels)
    plt.ylabel("Score")
    plt.title("Student Distribution of Types")
    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

    name = 'app/assets/images/summary.png'
    plt.savefig(name, bbox_inches='tight')

def main():
    student_graph(sys.argv[1:])

if __name__ == "__main__":
    main()
