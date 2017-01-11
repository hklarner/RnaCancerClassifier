

import os
import sys
sys.path.insert(0,'../')

import interfaces


def run():

    if 1:
        folder = '10x10_500x500_10x10_binomial_kobi_gates-inputs_10m'
        TYPE = 'benchmark'
    else:
        folder = '10x10_500x500_10x10_kobi_kobi_feasible_10m_10-fold-cv'
        TYPE = 'crossvalidation'
    

    times = []

    if TYPE=='benchmark':
        data = interfaces.files.read_benchmark_folder(folder)
        KEY = 'time'
        xKEY = 'solution'
        
    else:
        data = interfaces.files.read_crossvalidation_folder(folder)
        KEY = 'error'


    times = [x['time'] for x in data.values() if not x['time']==None]
    print 'max:', max(times)
    print 'min:', min(times)

    
    return 
    for pos, dic in data.items():
        print('{X}, {Y}'.format(X=pos, Y=dic[KEY]))


    return

    matrix, gateinputs = interfaces.files.read_dataset('tests/50x60')
    fname_csv = 'tests/50x60.csv'
    fname_asp = 'tests/50x60.asp'
    fname_res = 'tests/50x60.result'

    interfaces.files.write_csvfile(fname_csv, matrix, gateinputs)
    interfaces.potassco.create_aspfile(FnameCSV  = fname_csv,
                                       FnameASP  = fname_asp,
                                       TemplateClassifier = 'kobi',
                                       TemplateObjective  = 'inputs-gates')

    time, solution = interfaces.potassco.timed_call_single_solution(fname_asp, TimeOut='5m')
    print time
    print solution
    interfaces.files.write_benchmarkfile(fname_res, time, solution)



if __name__=='__main__':
    run()
