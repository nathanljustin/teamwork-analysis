# muddersOnRails()
# Maeve Murphy November 15, 2017
# Last updated: 11-16-17

# creates a histogram that shows the number of students with
# primary, secondary, tertiary, and quarternary rankings
# of each type.

# resources:
# https://matplotlib.org/examples/pylab_examples/bar_stacked.html
# https://chrisalbon.com/python/matplotlib_grouped_bar_plot.html


import pandas as pd
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


def make_adjacent_graph(primaries, secondaries, tertiaries, quarternaries):
    """Given all the prominences of styles from the style table in the
        database, create a adjacent bar graph to aggregate the information
        into one place by stacknig them in a histogram."""
    x_labels = [Style(x).name for x in range(len(Style))]
    print(x_labels,primaries,secondaries,tertiaries,quarternaries)

    raw_data = {'styles': ['Communicator', 'Collaborator','Challenger', 'Contributor'],
        'primary': primaries,
        'secondary': secondaries,
        'tertiary': tertiaries,
        'quarternary': quarternaries}
    df = pd.DataFrame(raw_data, columns = ['styles', 'primary', 'secondary', 'tertiary', 'quarternary'])

    # Setting the positions and width for the bars
    pos = list(range(len(df['styles'])))
    width = 0.2

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10,5))

    # Create a bar with primary data,
    # in position pos,
    plt.bar(pos,
            df['primary'],
            width,
            alpha=0.5,
            color='#82ccc4',
            label=df['styles'][0])

    # Create a bar with secondary data,
    # in position pos + some width buffer,
    plt.bar([p + width for p in pos],
            df['secondary'],
            width,
            alpha=0.5,
            color='#777ea8',
            label=df['styles'][1])

    # Create a bar with tertiary data,
    # in position pos + some width buffer,
    plt.bar([p + width*2 for p in pos],
            df['tertiary'],
            width,
            alpha=0.5,
            color='#008081',
            label=df['styles'][2])
    # Create a bar with quarternary data,
    # in position pos + some width buffer,
    plt.bar([p + width*3 for p in pos],
            df['quarternary'],
            width,
            alpha=0.5,
            color='#c4d89e',
            label=df['styles'][3])


    # Set the y axis label
    ax.set_ylabel('Number of Students')

    # Set the chart's title
    ax.set_title('Survey Results in Order of Dominance')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['styles'])

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    maxHeight = max(max(df['primary']), max(df['secondary']), max(df['tertiary']), max(df['quarternary'])) + 1
    if maxHeight > 30:
        maxHeight += 2
    print("max y is", maxHeight)
    plt.ylim([0, maxHeight])#max(df['primary'], df['secondary'], df['tertiary'], df['quarternary']) + 1] )

    # Adding the legend and showing the plot
    plt.legend(['Primary', 'Secondary', 'Tertiary', 'Quaternary'], bbox_to_anchor=(1.05, 1), loc=2,borderaxespad=0.)
    # plt.show()
    plt.savefig('app/assets/images/overall.png', bbox_inches='tight')


def main():
    tuples        = get_style_tuples()
    primaries     = tally_nth(tuples, 1)
    secondaries   = tally_nth(tuples, 2)
    tertiaries    = tally_nth(tuples, 3)
    quarternaries = tally_nth(tuples, 4)

    make_adjacent_graph(primaries, secondaries, tertiaries, quarternaries)

if __name__ == "__main__":
	main()
