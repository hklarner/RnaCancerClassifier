
from __future__ import print_function

import os
import sys
import distutils.dir_util
import shutil

import interfaces


def run():
    args = sys.argv[1:]

    if not args:
        print('Usage: python run_crossvalidation.py [DATASET] [CLASSIFIER] [OBJECTIVE] [TIMEOUT]')
        print('')
        print(' creates the folder crossvalidations/DATASET_TIMEOUT with results files')
        print('')
        print('DATASET is the name of a folder in datasets (e.g. 20x20_100x100_5x5_all-positive)')
        print('CLASSIFIER is the name of a file in templates/classifiers (e.g. all-positive)')
        print('OBJECTIVE is the name of a file in templates/objectives (e.g. beerenwinkel)')
        print('TIMEOUT is the duration before timeout of Potassco (see linux command "timeout" for syntax)')
        print('')
        print('Example:')
        print(' python run_crossvalidation.py 20x20_100x100_5x5_all-positive 10m')
        return

    if not len(args)==4:
        print(args)
        print('error: need exactly 4 arguments')
        return

    print('\nwelcome to run_crossvalidation.py')
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

    path_crossvalidation = 'crossvalidations/{DATASET}_{TIMEOUT}'.format(DATASET=DATASET, TIMEOUT=TIMEOUT)
    if os.path.exists(path_crossvalidation):
        print(' {PATH} is replaced'.format(PATH=path_crossvalidation))
        shutil.rmtree(path_crossvalidation)
    else:
        print(' {PATH} is created from scratch..'.format(PATH=path_crossvalidation))

    os.mkdir(path_crossvalidation)

    # info
    print(' timeout: {X}'.format(X=TIMEOUT))
    print(' files:   {X}'.format(X=len([x for x in os.listdir(path_dataset) if '~' not in x])))
            
    counter = 0
    for file_dataset in os.listdir(path_dataset):
        if '~' in file_dataset: continue
        if '.' in file_dataset: continue

        full_matrix, gateinputs_annotation = interfaces.files.read_dataset(os.path.join(path_dataset, file_dataset))

        with interfaces.files.nostdout():
            function_annotation = interfaces.boolean_functions.gateinputs2function(gateinputs_annotation)
    
        mismatches = 0.0
        time_total = 0.0
        for matrix, row in interfaces.crossvalidation.leave_one_out_generator(full_matrix):

            fname_csv = os.path.join(path_crossvalidation, file_dataset+'.csv')
            fname_asp = os.path.join(path_crossvalidation, file_dataset+'.asp')

            interfaces.files.write_csvfile(fname_csv, matrix, gateinputs_annotation)
            interfaces.potassco.create_aspfile(FnameCSV  = fname_csv,
                                               FnameASP  = fname_asp,
                                               TemplateClassifier = CLASSIFIER,
                                               TemplateObjective  = OBJECTIVE)


            time, gateinputs_solution = interfaces.potassco.timed_call_single_solution(fname_asp, TimeOut=TIMEOUT)
            time_total+= interfaces.plotting.time2int(time)
            
            if not gateinputs_solution:
                mismatches+= 1
                continue
            
            with interfaces.files.nostdout():
                function_solution = interfaces.boolean_functions.gateinputs2function(gateinputs_solution)

            row_data = interfaces.files.row2dict(row)
            if function_annotation(row_data) != function_solution(row_data):
                mismatches+= 1

        performance = mismatches / len(full_matrix)

        fname_result = os.path.join(path_crossvalidation, file_dataset+'.result')

        interfaces.files.write_crossvalidationfile(fname_result, performance, time_total)

        counter+= 1

    print(' done:    created {X} files in {PATH}'.format(X=counter,PATH=path_crossvalidation))
    
    
    
    




if __name__ == '__main__':
    run()
