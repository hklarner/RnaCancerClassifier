
from __future__ import print_function

import shutil
import os
import sys
import random
import interfaces


def run():
    print('\nwelcome to create_dataset.py')

    args = sys.argv[1:]

    if not args:
        print(' Usage: python create_dataset.py [FROM] [TO] [SKIP] [CLASSIFIER]')
        print('')
        print('  creates a folder datasets/FROM_TO_CLASSIFIER that contains files 20x20, 21x20, ...')
        print('  each with a 0-1 matrix of the specified dimensions, followed by a classifier')
        print('')
        print(' FROM is the smallest data matrix (e.g. 20x20)')
        print(' TO is the largest data matrix (e.g. 100x100)')
        print(' SKIP is the x and y increase (e.g. 5x5)')
        print(' CLASSIFIER is the name of a classifier template for annotation (file in templates/classifiers)')
        print('')
        print(' Example:')
        print('  python create_dataset.py 20x20 100x100 5x5 all-positive')
        return

    if not len(args)==4:
        print('error: need exactly 4 arguments but got "{X}", stopping.'.format(X=args))
        return

    FROM, TO, SKIP, CLASSIFIER = args

    from_x, from_y = map(int,FROM.split('x'))
    to_x, to_y = map(int,TO.split('x'))
    skip_x, skip_y = map(int,SKIP.split('x'))
    
    if (to_x-from_x)%skip_x:
        print(' error: skip in tissues doesnt divide the range: ({X}-{Y})%{Z}!=0, stopping.'.format(X=to_x,Y=from_x,Z=skip_x))
        return

    if (to_y-from_y)%skip_y:
        print(' error: skip in miRNAs doesnt divide the range: ({X}-{Y})%{Z}!=0, stopping.'.format(X=to_y,Y=from_y,Z=skip_y))
        return

    if '_' in CLASSIFIER:
        print('error: underscore is not allowed in template {X}, stopping.'.format(X=CLASSIFIER))
        return

    
    path_dataset = 'datasets/{FROM}_{TO}_{SKIP}_{CLASSIFIER}'.format(FROM=FROM,TO=TO,SKIP=SKIP,CLASSIFIER=CLASSIFIER)
    if os.path.exists(path_dataset):
        print(' {PATH} is replaced'.format(PATH=path_dataset))
        shutil.rmtree(path_dataset)
    else:
        print(' {PATH} is created'.format(PATH=path_dataset))
        
    os.mkdir(path_dataset)
             
    counter = 0
    print(' creating data sets..', end='')

    
    
    for x in range(from_x, to_x+1, skip_x):
        for y in range(from_y, to_y+1, skip_y):
            
            matrix = interfaces.matrices.create_matrix(x, y)
            classifier = interfaces.boolean_functions.create_random_classifier(CLASSIFIER, MaxMiRNAs=y)

            fname_dataset = '{ROWS}x{COLS}'.format(ROWS=x,COLS=y)
            path = os.path.join(path_dataset,fname_dataset)
            interfaces.files.write_dataset(path, matrix, classifier)
            
            counter+= 1

    print(' done.')
    print(' created {X} files in datasets/{FROM}_{TO}_{SKIP}_{CLASSIFIER}'.format(X=counter,FROM=FROM,TO=TO,SKIP=SKIP,CLASSIFIER=CLASSIFIER))
            

                



if __name__ == '__main__':
    run()
