
from __future__ import print_function

import os
import sys
import distutils.dir_util
import shutil
import importlib

import interfaces


def run():
    print('\nwelcome to run_crossvalidation.py')
    
    args = sys.argv[1:]

    if not args:
        print(' Usage: python run_crossvalidation.py [TEMPLATE] [DATASET] [CLASSIFIER] [OBJECTIVE] [TIMEOUT]')
        print('')
        print('  creates the folder crossvalidations/DATASET_TIMEOUT with results files')
        print('')
        print(' TEMPLATE is the name of a file in templates/crossvalidation (e.g. leave-one-out)')
        print(' DATASET is the name of a folder in datasets (e.g. 20x20_100x100_5x5_all-positive)')
        print(' CLASSIFIER is the name of a file in templates/classifiers (e.g. all-positive)')
        print(' OBJECTIVE is the name of a file in templates/objectives (e.g. beerenwinkel)')
        print(' TIMEOUT is the duration before timeout of Potassco (see linux command "timeout" for syntax)')
        print('')
        print(' Example:')
        print('  python run_crossvalidation.py leave-one-out 20x20_100x100_5x5_kobi kobi feasible 10m')
        return

    if not len(args)==5:
        print(' error: need exactly 5 arguments but got "{X}", stopping.'.format(X=args))
        return

    TEMPLATE, DATASET, CLASSIFIER, OBJECTIVE, TIMEOUT = args

    if '_' in CLASSIFIER:
        print('error: underscore is not allowed in template {X}, stopping.'.format(X=CLASSIFIER))
        return

    if '_' in OBJECTIVE:
        print('error: underscore is not allowed in template {X}, stopping.'.format(X=OBJECTIVE))
        return


    try:
        VALIDATER = importlib.import_module('templates.crossvalidations.{X}'.format(X=TEMPLATE))
        
    except Exception as EX:
        print(' can not import templates.crossvalidations.{X} because "{Y}", stopping.'.format(X=TEMPLATE, Y=EX))
        raise Exception

    
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

    path_template = os.path.join('crossvalidations', TEMPLATE)
    if not os.path.exists(path_template):
        print(' creating crossvalidations/{PATH}/'.format(PATH=path_template))
        os.mkdir(path_template)

    path_crossvalidation = 'crossvalidations/{DATASET}_{CLASSIFIER}_{OBJECTIVE}_{TIMEOUT}_{TEMPLATE}'.format(DATASET=DATASET,
                                                                                                             CLASSIFIER=CLASSIFIER,
                                                                                                             OBJECTIVE=OBJECTIVE,
                                                                                                             TIMEOUT=TIMEOUT,
                                                                                                             TEMPLATE=TEMPLATE)
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

        function_annotation = interfaces.boolean_functions.gateinputs2function(gateinputs_annotation)
        error_total = 0.0
        time_total  = 0.0
        
        for matrix, test_data in VALIDATER.generator(full_matrix):

            fname_csv = os.path.join(path_crossvalidation, file_dataset+'.csv')
            fname_asp = os.path.join(path_crossvalidation, file_dataset+'.asp')

            interfaces.files.write_csvfile(fname_csv, matrix, gateinputs_annotation)
            interfaces.potassco.create_aspfile(FnameCSV  = fname_csv,
                                               FnameASP  = fname_asp,
                                               TemplateClassifier = CLASSIFIER,
                                               TemplateObjective  = OBJECTIVE)

            
            time, gateinputs_solution = interfaces.potassco.timed_call_single_solution(fname_asp, TimeOut=TIMEOUT)

            if time==None:
                # timeout, add maximal time
                time_total+= interfaces.plotting.time2int(TIMEOUT)
            else:
                # no timeout, add precise time
                time_total+= interfaces.plotting.time2int(time)


            if gateinputs_solution==None:
                # no solution, get default error for test data
                error = VALIDATER.get_error_for_no_solution(function_annotation, test_data)
            else:
                # solution, compute error for test data
                function_solution = interfaces.boolean_functions.gateinputs2function(gateinputs_solution)
                error = VALIDATER.get_error(function_annotation, function_solution, test_data)

            error_total+= error

            os.remove(fname_csv)
            os.remove(fname_asp)


        error = VALIDATER.get_generalization_error(error_total, full_matrix)
        fname_result = os.path.join(path_crossvalidation, file_dataset+'.result')
        interfaces.files.write_crossvalidation_file(fname_result, error, time_total)
        counter+= 1

    print(' done:    created {X} files in {PATH}'.format(X=counter,PATH=path_crossvalidation))
    
    
    
    




if __name__ == '__main__':
    run()
