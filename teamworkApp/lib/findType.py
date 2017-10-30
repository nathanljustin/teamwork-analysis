def getType(scores):
    """ Find student's type(s) based on survey answers
    """
    maxScore = 0
    studentType = []

    # Get best scores
    for i in range(len(scores)):
        if scores[i] >= maxScore - 3:
            studentType += [i]
        if scores[i] > maxScore:
            maxScore = scores[i]
            if scores[i] - 3 > maxScore:
                studentType = [i]
    
    return tuple(studentType)
