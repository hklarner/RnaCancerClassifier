

import interfaces


def generator(Matrix):
    for x in range(len(Matrix)):
        new_matrix = [row for y,row in enumerate(Matrix) if x!=y]
        row = Matrix[x]
        
        yield new_matrix, row
        
        

def get_error(FunctionAnnotation, FunctionSolution, TestData):
    row = interfaces.files.row2dict(TestData)

    if FunctionAnnotation(row)==FunctionSolution(row):
        return 0

    return 1


def get_error_for_no_solution(FunctionAnnotation, TestData):
    return 1

def get_generalization_error(TotalError, Matrix):

    return 1.*TotalError / len(Matrix)
