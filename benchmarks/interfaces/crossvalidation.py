



def leave_one_out_generator(Matrix):
    for x in range(len(Matrix)):
        new_matrix = [row for y,row in enumerate(Matrix) if x!=y]
        row = Matrix[x]
        
        yield new_matrix, row
        
        

