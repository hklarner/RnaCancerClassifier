

import sys
import os
import importlib

import interfaces


def run():
    print('\nwelcome to create_plot.py')
    
    args = sys.argv[1:]

    if not args:
        print(' Usage: python create_plot.py [TEMPLATE] [TYPE] [FOLDER]')
        print('')
        print(' TYPE is either "benchmark" or "crossvalidation"')
        print(' FOLDER is the name of a folder of results files (e.g. 20x20_100x100_all-positive)')
        print(' TEMPLATE is the name of a file in templates/plots (e.g. surface2d)')
        print('')
        print(' Example:')
        print('  python create_plot.py 20x20_100x100_all-positive scatter3D')
        return

    if not len(args)==3:
        print(' error: need exactly 3 arguments but got "{X}", stopping.'.format(X=args))
        return

    TEMPLATE, TYPE, FOLDER = args

    # check names
    if not TYPE in ['benchmark','crossvalidation']:
        print(' TYPE must be either "benchmark" or "crossvalidation", not "{X}", stopping.'.format(X=TYPE))
        return

    path_results = os.path.join(TYPE+'s',FOLDER)

    print(' reading {X}'.format(X=path_results))

    if not os.path.exists(path_results):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_results))
        return

    path_type = os.path.join('plots',TYPE)
    if not os.path.exists(path_type):
        print(' creating {X}.'.format(X=path_type))
        os.mkdir(path_type)
    try:
        PLOTTER = importlib.import_module('templates.plots.{X}'.format(X=TEMPLATE))
        
    except Exception as EX:
        print(' can not import templates.plots.{X} because "{Y}", stopping.'.format(X=TEMPLATE, Y=EX))
        raise Exception

    
    if TYPE=='benchmark':
        array = interfaces.files.read_benchmark_folder(FOLDER)
        PLOTTER.run(TYPE, FOLDER, array)

    elif TYPE=='crossvalidation':
        array = interfaces.files.read_crossvalidation_folder(FOLDER)
        PLOTTER.run(TYPE, FOLDER, array)

    else:
        print(' error: Type "{X}" not known.'.format(X=TYPE))
        return
        
    
    




if __name__=="__main__":
    run()
