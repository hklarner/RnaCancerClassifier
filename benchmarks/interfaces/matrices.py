

import random


def create_matrix(Rows, Columns):
    matrix = []
    for x in range(Rows):
        matrix.append(''.join(random.choice('01') for i in range(Columns)))

    return '\n'.join(matrix)
