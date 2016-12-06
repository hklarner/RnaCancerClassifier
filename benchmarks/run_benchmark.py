
from __future__ import print_function

import os
import sys
import distutils.dir_util
import shutil

import interfaces


def run():
    args = sys.argv[1:]

    if not args:
        print('Usage: python run_benchmark.py [DATASET] [CLASSIFIER] [OBJECTIVE] [TIMEOUT]')
        print('')
        print(' creates the folder benchmarks/DATASET_CLASSIFIER_OBJECTIVE_TIMEOUT with results files')
        print('')
        print('DATASET is the name of a folder in datasets (e.g. 20x20_100x100_all-positive)')
        print('CLASSIFIER is the name of a file in templates/classifiers (e.g. all-positive)')
        print('OBJECTIVE is the name of a file in templates/objectives (e.g. beerenwinkel)')
        print('TIMEOUT is the duration before timeout of Potassco (see linux command "timeout" for syntax)')
        print('')
        print('Example:')
        print(' python run_benchmark.py 20x20_100x100_all-positive all-positive beerenwinkel 10m')
        return

    if not len(args)==4:
        print(args)
        print('error: need exactly 4 arguments')
        return

    print('\nwelcome to run_benchmark.py')
    DATASET, CLASSIFIER, OBJECTIVE, TIMEOUT = args

    if '_' in CLASSIFIER:
        print('error: underscore is not allowed in template {X}, stopping.'.format(X=CLASSIFIER))
        return

    if '_' in OBJECTIVE:
        print('error: underscore is not allowed in template {X}, stopping.'.format(X=OBJECTIVE))
        return

    # checking paths
    path_dataset = 'datasets/{DATASET}'.format(DATASET=DATASET)
    if not os.path.exists(path_dataset):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_dataset))
        return

    path_classifier = 'templates/classifiers/{CLASSIFIER}.py'.format(CLASSIFIER=CLASSIFIER)
    if not os.path.exists(path_classifier):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_classifier))
        return

    path_objective = 'templates/objectives/{OBJECTIVE}.py'.format(OBJECTIVE=OBJECTIVE)
    if not os.path.exists(path_objective):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_objective))
        return

    path_benchmark = 'benchmarks/{DATASET}_{CLASSIFIER}_{OBJECTIVE}_{TIMEOUT}'.format(DATASET=DATASET, CLASSIFIER=CLASSIFIER,
                                                                                      OBJECTIVE=OBJECTIVE, TIMEOUT=TIMEOUT)
    if os.path.exists(path_benchmark):
        print(' {PATH} is replaced'.format(PATH=path_benchmark))
        shutil.rmtree(path_benchmark)
    else:
        print(' {PATH} is created from scratch..'.format(PATH=path_benchmark))

    os.mkdir(path_benchmark)

    # info
    print(' timeout: {X}'.format(X=TIMEOUT))
    print(' files:   {X}'.format(X=len([x for x in os.listdir(path_dataset) if '~' not in x])))
            
    counter = 0
    for file_dataset in os.listdir(path_dataset):
        if '~' in file_dataset: continue
        if '.' in file_dataset: continue

        matrix, gateinputs = interfaces.files.read_dataset(os.path.join(path_dataset, file_dataset))

        fname_csv = os.path.join(path_benchmark, file_dataset+'.csv')
        fname_asp = os.path.join(path_benchmark, file_dataset+'.asp')

        interfaces.files.write_csvfile(fname_csv, matrix, gateinputs)
        interfaces.potassco.create_aspfile(FnameCSV  = fname_csv,
                                           FnameASP  = fname_asp,
                                           TemplateClassifier = CLASSIFIER,
                                           TemplateObjective  = OBJECTIVE)

        time, solution = interfaces.potassco.timed_call_single_solution(fname_asp, TimeOut=TIMEOUT)

        os.remove(fname_csv)
        os.remove(fname_asp)

        fname_result = os.path.join(path_benchmark, file_dataset+'.result')

        interfaces.files.write_benchmarkfile(fname_result, time, solution)
        
        counter+= 1

    print(' done:    created {X} files in {PATH}'.format(X=counter,PATH=path_benchmark))
    
    
    
    




if __name__ == '__main__':
    run()
