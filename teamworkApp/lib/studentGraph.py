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
import os
import dbCalls
from evaluateAnswers import Style


def make_averages(score_set, y_pos, labels):
    """
    Creates a graph of the average score for each style of each student selected

    input:
        score_set: the student scores
        y_pos: the arange of labels
        labels: each of the styles
    """
    avgScores = [float(sum(col))/len(col) for col in zip(*score_set)]
    plt.bar(y_pos, avgScores, align = 'center', color='#3fe0d0', alpha = 0.5, label = 'Average Values')

    # Make graph
    plt.xticks(y_pos, labels)
    plt.ylabel("Score")
    plt.title("Average Student Distribution of Types")
    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )


    average_graph = 'app/assets/images/average.png'
    plt.savefig(average_graph, bbox_inches='tight')
    plt.cla()



def make_grouped(score_set, y_pos, labels, names):
    """
    Creates a grouped bar graph of the score for each style of each student selected

    input:
        score_set: the student scores
        y_pos: the arange of labels
        labels: each of the styles
        names: usernames of the students selected
    """
    # change for each set of bars
    width_change = -0.4
    width = 0.8/len(score_set)
    colors = ['#3fe0d0', '#111e6c', '#008081', '#a3de38', '#3378e8', '#8733e8']
    curr_iter = 0

    for scores in score_set:
        username = names[curr_iter][0]
        plt.bar(y_pos + width_change, scores, width = width, color = colors[curr_iter],  align='edge', alpha = 0.5, label = username)
        width_change += width
        curr_iter += 1
        
    # Make graph
    plt.xticks(y_pos, labels)
    plt.ylabel("Score")
    plt.title("Student Distribution of Types")
    plt.legend( bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )

    grouped_graph = 'app/assets/images/grouped.png'
    plt.savefig(grouped_graph, bbox_inches='tight')



def student_graph(student_ids):
    """Returns a path to where the student's graph is saved"""
    # remove the grouped bar graph in case the next selection size will
    # be greater than 6 students
    try:
        os.remove('app/assets/images/grouped.png')
    except OSError:
        pass

    labels = [Style(x).name for x in range(len(Style))]
    names = dbCalls.get_names(student_ids)
    # Connect to db to get scores
    db_data = dbCalls.get_students_styles(student_ids)
    y_pos = np.arange(len(labels))
    score_set = [data[2:6] for data in db_data]

    # Get the scores needed
    assert(len(db_data) != 0), "Cannot find student data."
    make_averages(score_set, y_pos, labels)

    # create split bar graph if <= 6 students
    if len(score_set) <= 6:
        make_grouped(score_set, y_pos, labels, names)


def main():
    student_graph(sys.argv[1:])

if __name__ == "__main__":
    main()
