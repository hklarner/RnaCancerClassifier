

import sys
import os
import importlib

import interfaces


def run():
    args = sys.argv[1:]

    if not args:
        print('Usage: python create_plot.py [BENCHMARK] [PLOT]')
        print('')
        print('BENCHMARK is the name of a folder in benchmarks (e.g. 20x20_100x100_all-positive)')
        print('PLOT is the name of a file in templates/plots (e.g. basic)')
        print('pass special keyword ALL to BENCHMARK to create a plot for every benchmark')
        print('')
        print('Example:')
        print(' python create_plot.py 20x20_100x100_all-positive scatter3D')
        print(' python create_plot.py ALL surface2D')
        return

    if not len(args)==2:
        print(args)
        print('error: need exactly 2 arguments')
        return

    BENCHMARK, PLOT = args

    print('\nwelcome to create_plot.py')

    # check names
    if not BENCHMARK=='ALL':
        print(' reading {X}'.format(X=BENCHMARK))
        path_benchmark = 'benchmarks/{BENCHMARK}'.format(BENCHMARK=BENCHMARK)
        if not os.path.exists(path_benchmark):
            print(' {PATH} does not exist, stopping.'.format(PATH=path_benchmark))
            return

    path_plot = 'templates/plots/{PLOT}.py'.format(PLOT=PLOT)
    if not os.path.exists(path_plot):
        print(' {PATH} does not exist, stopping.'.format(PATH=path_plot))
        return

    try:
        PLOTTER = importlib.import_module('templates.plots.{X}'.format(X=PLOT))
        
    except Exception as EX:
        print(EX)
        print(' >> could not import {X}'.format(X=path_plot))
        raise Exception

    
    
    if BENCHMARK=='ALL':
        hit = False
        for folder in os.listdir('benchmarks'):
            hit = True
            print(' reading {X}'.format(X=folder))
            array = interfaces.files.read_benchmarks(folder)

            if not array:
                print(' no files for {X}, stopping'.format(X=os.path.join('benchmarks',folder)))
                continue
            
            PLOTTER.run(folder, array)
            print(' created {X}_{P}.pdf'.format(X=folder, P=PLOT))
        if not hit:
            print(' benchmarks/ is empty, stopping.')
            
    else:
        array = interfaces.files.read_benchmarks(BENCHMARK)
        PLOTTER.run(BENCHMARK, array)
        print(' created {X}_{P}.pdf'.format(X=BENCHMARK, P=PLOT))
    
    




if __name__=="__main__":
    run()
