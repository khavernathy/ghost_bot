import numpy as np


# metric for similarity between strings for typo-fix
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    #print (matrix)
    lev = (matrix[size_x - 1, size_y - 1])

    # determine if the strings "should be" the same or nah
    # small words should have tighter criteria
    if len(seq1) < 4 or len(seq2) < 4:
        if lev == 1:
            return True
    # two characters off is okay if the word(s) is 4+ letters i guess
    elif lev < 3:
        return True
    else:
        return False
