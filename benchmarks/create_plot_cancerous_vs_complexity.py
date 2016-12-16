

import sys
import os
import importlib

import interfaces

import templates.plots.cancerous_vs_complexity
    

def run():
    print('\nwelcome to plot_cancerous_vs_complexity.py')
    
    args = sys.argv[1:]

    if not args:
        print(' Usage: python create_cancerous_vs_complexity_plot.py [FOLDER]')
        print('')
        print(' FOLDER is the name of a crossvalidations folder (e.g. 10x10_500x500_10x10_kobi_kobi_feasible_10m_10-fold-cv)')
        print('')
        print(' Example:')
        print('  python create_cancerous_vs_complexity_plot.py 10x10_500x500_10x10_kobi_kobi_feasible_10m_10-fold-cv')
        return

    if not len(args)==1:
        print(' error: need exactly 1 argument but got "{X}", stopping.'.format(X=args))
        return

    FOLDER_BENCHMARK = args.pop()
    FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT = FOLDER_BENCHMARK.split('_')
    FOLDER_DATASET = '_'.join([FROM, TO, SKIP, CLASSIFIER_ANNOTATION])

    # check names

    path_benchmark = os.path.join('benchmarks',FOLDER_BENCHMARK)

    print(' reading {X}'.format(X=path_benchmark))

    if not os.path.exists(path_benchmark):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_benchmark))
        return

    path_data = os.path.join('datasets',FOLDER_DATASET)

    print(' reading {X}'.format(X=path_data))

    if not os.path.exists(path_data):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_data))
        return


    array_benchmark = interfaces.files.read_benchmark_folder(FOLDER_BENCHMARK)
    array_dataset   = interfaces.files.read_dataset_folder(FOLDER_DATASET)
    templates.plots.cancerous_vs_complexity.run(FOLDER_BENCHMARK, array_benchmark, array_dataset)

        
    
    




if __name__=="__main__":
    run()
