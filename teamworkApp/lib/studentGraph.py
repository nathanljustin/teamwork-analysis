import argparse 
import matplotlib.pyplot as plt

from evaluateAnswers import * 

def student_graph(student_id):
    """Returns a path to where the student's graph is saved"""

    labels = [Style(x).name for x in range(len(Style))]
    scores = find_scores(student_id)

    fig1, ax1 = plt.subplots()
    ax1.pie(scores, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')

    name = 'tmp/summary' + str(student_id) + '.png'
    plt.savefig(name, bbox_inches='tight')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate graph summarizing a student's answers")
    parser.add_argument(
        'student_id', 
        type=int, 
        help='Student id for desired student graph',
    )
    args = parser.parse_args()

    student_graph(args.student_id)

