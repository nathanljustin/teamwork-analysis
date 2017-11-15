import argparse 
import matplotlib.pyplot as plt
import numpy as np

import dbCalls
from evaluateAnswers import Style

def student_graph(student_ids):
    """Returns a path to where the student's graph is saved"""

    labels = [Style(x).name for x in range(len(Style))]

    # Connect to db to get scores
    dbData = dbCalls.get_students_styles(student_ids)
    scoreSet = [data[2:6] for data in dbData]

    # Get the scores needed
    assert(len(dbData) != 0), "Cannot find student data."

    # Make graph
    labels = [Style(x).name for x in range(len(Style))]
    yPos = np.arange(len(labels))
    
    # create split bar graph if <= 4 students
    if len(scoreSet) <= 4:
        currStart = -0.4
        width = 0.8/len(scoreSet)
        colors = ['#3fe0d0', '#111e6c', '#008081', '#a3de38']
        currColor = 0
        for scores in scoreSet:
            plt.bar(yPos + widthChange, scoreSet, width = width, color = colors[currColor],  alpha = 0.5, label = scores)
            widthChange += width
            currColor += 1
    
    # create summary graph if > 4 students
    else:
        # find avg val for each score
        avgScores = [float(sum(col))/len(col) for col in zip(*scoreSet)]
        plt.bar(yPos, avgScores, align = 'center', alpha = 0.5, label = 'Average')

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
    plt.legend( loc='best' )

    name = 'app/assets/images/summary' + str(student_id) + '.png'
    plt.savefig(name, bbox_inches='tight')

def main():
    parser = argparse.ArgumentParser(description="Generate graph summarizing a student's answers")
    parser.add_argument(
        'student_id', 
        type=int, 
        help='Student id for desired student graph',
    )
    args = parser.parse_args()

    student_graph(args.student_id)

if __name__ == "__main__":
    main()
    