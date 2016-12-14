

import random
import interfaces


def generator(Matrix):
    assert(len(Matrix)>=10)

    matrix = list(Matrix)
    random.shuffle(matrix)

    chunk_size, remainder = divmod(len(Matrix),10)
    
    chunks = [matrix[i*chunk_size:(i+1)*chunk_size] for i in range(10-remainder)]
    chunks+= [matrix[i*chunk_size:(i+1)*chunk_size+1] for i in range(10-remainder,10)]

    for i in range(10):
        learningset = [y for x in chunks if not chunks.index(x)==i for y in x]
        testdata = chunks[i]


        yield learningset, testdata
                   

def get_error(FunctionAnnotation, FunctionSolution, TestData, Debug=False):

    error = 0
    for row in TestData:
        row = interfaces.files.row2dict(row)
        
        if Debug:
            print('row: {X}'.format(row))
            
        if FunctionAnnotation(row)==FunctionSolution(row):
            
            if Debug:
                print('FunctionAnnotation(row)={X}'.format(X=FunctionAnnotation(row)))
                print('FunctionSolution(row)=  {X}'.format(X=FunctionSolution(row)))
                
            error+=1

    return error


def get_error_for_no_solution(FunctionAnnotation, TestData):
    return len(TestData)


def get_generalization_error(TotalError, Matrix):

    return 1.*TotalError / len(Matrix)
