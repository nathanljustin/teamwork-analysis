############################
##      Deprecated       ##
###########################


# resources:

# muddersOnRails()
# Maeve Murphy October 12, 2017
# Last updated: 10-13-2017

# Simple function for creating a lot of data that can be written to
# the database
import random

POSSIBLE_RESPONSES = {"0": [1,2,3,4], "1": [1,2,4,3], "2": [1,3,2,4],
                     "3": [1,3,4,2], "4": [1,4,2,3], "5": [1,4,3,2],
                     "6": [2,1,3,4], "7": [2,1,4,3], "8": [2,3,1,4],
                     "9": [2,3,4,1], "10": [2,4,1,3], "11": [2,4,3,1],
                     "12": [3,1,2,4], "13": [3,1,4,2], "14": [3,2,1,4],
                     "15": [3,2,4,1], "16": [3,4,1,2], "17": [3,4,2,1],
                     "18": [4,1,2,3], "19": [4,1,3,2], "20": [4,2,1,3],
                     "21": [4,2,3,1], "22": [4,3,1,2], "23": [4,3,2,1]}

def generateData(numStudents):
    """Generates a list of students and their responses
    to the 18 questions in the survey.
    Inputs:
        numStudents, the number of students to generate data for
    Outputs:
        dictionary with keys being the students and values being a list of
        lists corresponding to the student's response.
    All responses are randomly generated"""
    studentData = {}
    for i in range(0,numStudents):
        responseList = []
        for question in range(0,18):
            # fetch a response from POSSIBLE_RESPONSES based on a random
            # integer from 0 to 23
            response = POSSIBLE_RESPONSES[str(random.choice(range(0,23)))]
            responseList += [response]
        # generate an anonymized name for each student
        studentName = 'S'+ str(i)
        # add the responses to the dictionary
        studentData[studentName] = responseList
    return studentData
