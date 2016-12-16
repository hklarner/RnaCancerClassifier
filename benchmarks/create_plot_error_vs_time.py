

import sys
import os
import importlib

import interfaces

import templates.plots.error_vs_time


def run():
    print('\nwelcome to create_error_vs_time_plot.py')
    
    args = sys.argv[1:]

    if not args:
        print(' Usage: python create_error_vs_time_plot.py [FOLDER]')
        print('')
        print(' FOLDER is the name of a crossvalidations folder (e.g. 10x10_500x500_10x10_kobi_kobi_feasible_10m_10-fold-cv)')
        print('')
        print(' Example:')
        print('  python create_error_plot.py 10x10_500x500_10x10_kobi_kobi_feasible_10m_10-fold-cv')
        return

    if not len(args)==1:
        print(' error: need exactly 1 argument but got "{X}", stopping.'.format(X=args))
        return

    FOLDER = args.pop()

    # check names

    path_results = os.path.join('crossvalidations',FOLDER)

    print(' reading {X}'.format(X=path_results))

    if not os.path.exists(path_results):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_results))
        return


    array = interfaces.files.read_crossvalidation_folder(FOLDER)
    templates.plots.error_vs_time.run(FOLDER, array)

        
    
    




if __name__=="__main__":
    run()
