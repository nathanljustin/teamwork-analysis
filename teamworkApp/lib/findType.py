############################
##      Deprecated?      ##
###########################

def getType(scores):
    """ Find student's type(s) based on survey answers
    """
    maxScore = max(scores)
    studentType = []

    # Get best scores
    for i in range(len(scores)):
        if scores[i] >= maxScore - 3:
            studentType += [i]
    return tuple(studentType)
