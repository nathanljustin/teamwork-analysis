import argparse 
import matplotlib.pyplot as plt
import numpy as np

import dbCalls
from evaluateAnswers import Style

# TODO: Talk to team, determine if we want to continue taking in input in the method we are now, i.e. '0123', instead of ['0','1','2','3']

def student_graph(student_ids):
    """Returns a path to where the student's graph is saved"""

    labels = [Style(x).name for x in range(len(Style))]
    # Connect to db to get scores
    # TODO: At the moment, this seems to only return 1 from the list
    dbData = dbCalls.get_students_styles(student_ids)

    yPos = np.arange(len(labels))
    scoreSet = [data[2:6] for data in dbData]
    # Get the scores needed
    assert(len(dbData) != 0), "Cannot find student data."

    # create split bar graph if <= 4 students
    if len(scoreSet) <= 4:
        # change for each set of bars
        widthChange = 0 - 0.1*(len(scoreSet) - 1)
        width = 0.8/len(scoreSet)
        colors = ['#3fe0d0', '#111e6c', '#008081', '#a3de38']
        currIter = 0
        for scores in scoreSet:
            username = dbCalls.get_name(student_ids[currIter]) # TODO: doesn't function right now. 
            plt.bar(yPos + widthChange, scores, width = width, color = colors[currIter],  align='center', alpha = 0.5, label = username)
            widthChange += width
            currIter += 1
    
    # create summary graph if > 4 students
    else:
        # find avg val for each score
        avgScores = [float(sum(col))/len(col) for col in zip(*scoreSet)]
        plt.bar(yPos, avgScores, align = 'center', color='#3fe0d0', alpha = 0.5, label = 'Average Values')

    # Make graph
    plt.xticks(yPos, labels)
    plt.ylabel("Score")
    plt.title("Student Distribution of Types")
    plt.legend( loc='best' )

    name = 'app/assets/images/summary.png'
    plt.savefig(name, bbox_inches='tight')

def main():
    parser = argparse.ArgumentParser(description="Generate graph summarizing a student's answers")
    parser.add_argument(
        'student_id', 
        type=list, 
        help='Student id for desired student graph',
    )
    args = parser.parse_args()
    student_graph(args.student_id)

if __name__ == "__main__":
    main()
    