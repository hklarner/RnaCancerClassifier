
import interfaces

import os
import sys
sys.path.insert(0,'../')
import classifier as CLASSIFIER_SCRIPT

import cStringIO
import contextlib

import numpy

@contextlib.contextmanager
def nostdout():
    """ taken from: http://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto"""
    save_stdout = sys.stdout
    sys.stdout = cStringIO.StringIO()
    yield
    sys.stdout = save_stdout
        

def write_dataset(FnameData, Matrix, GateInputs):

    with open(FnameData,'w') as f:
        f.write(Matrix)
        f.write('\n\n')
        f.write(GateInputs)


def read_dataset(FnameData):

    matrix = []
    with open(FnameData, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line: continue
        if 'gate' in line:
            gateinputs = line
        else:
            matrix.append([x for x in line])

    return matrix, gateinputs


def write_csvfile(FnameCSV, Matrix, GateInputs):

    col_width = len(str(len(Matrix[0])))+5
    
    mirnas = ['g{i}'.format(i=i) for i in range(1,len(Matrix[0])+1)]
    header = ''.join(['   ID, ','Annots,'] + [x.rjust(col_width,' ') for x in mirnas])
    for i in range(10):
        header = header.replace('%i '%i,'%i,'%i)
    ids    = [str(i) for i in range(1,len(Matrix[0])+1)]

    with nostdout():
        function = interfaces.boolean_functions.gateinputs2function(GateInputs)
    
    with open(FnameCSV, 'w') as f:
        f.write(header)
        f.write('\n')

        for ID, row in enumerate(Matrix):
            sampledict = dict(zip(ids,row))
            sampledict['ID'] = str(ID+1)
            
            line = '{X},'.format(X=ID+1)
            line = line.rjust(6,' ')+' '
            line+= '{X}      '.format(X=function(sampledict))
            line+= ''.join(x.rjust(col_width,' ') for x in row)
            line = line.replace('0 ','0,')
            line = line.replace('1 ','1,')

            f.write(line)
            f.write('\n')


def row2dict(Row):
    #mirnas = ['g{i}'.format(i=i) for i in range(1,len(Row)+1)]
    #header = ''.join(['ID,','Annots,'] + [x for x in mirnas])
    
    ids1    = ['g%i'%i for i in range(1,len(Row)+1)]
    ids2    = [str(i) for i in range(1,len(Row)+1)]

    result = dict(zip(ids1,Row)+zip(ids2,Row))
    result['ID'] = 'None'

    return result


def write_benchmark_file(Fname, Time, Solution):
    lines = ['solution: {X}'.format(X=Solution),
             'time:     {X}'.format(X=Time)]
    
    with open(Fname,'w') as f:
        f.write('\n'.join(lines))


def read_benchmark_file(Fname):

    with open(Fname,'r') as f:
        lines = f.readlines()

    assert(len(lines)==2)
    solution = lines[0].split(':')[1].strip()
    time     = lines[1].split(':')[1].strip()

    return {'time':time, 'solution':solution}

    
def read_benchmark_folder(Folder):

    # dictionary
    path = os.path.join('benchmarks', Folder)
    array = {}
    for fname in os.listdir(path):
        if not fname.endswith('.result'): continue
        if '~' in fname: continue

        pos = tuple(map(int,fname.split('.')[0].split('x')))

        path = os.path.join('benchmarks', Folder, fname)
        array[pos] = read_benchmark_file(path)

    return array


def write_crossvalidation_file(Fname, Performance, Time):
    lines = ['performance: {X}'.format(X=Performance),
             'time:        {X}'.format(X=Time)]
    
    with open(Fname,'w') as f:
        f.write('\n'.join(lines))
    

def read_crossvalidation_file(Fname):

    with open(Fname,'r') as f:
        lines = f.readlines()

    assert(len(lines)==2)
    performance = lines[0].split(':')[1].strip()
    time        = lines[1].split(':')[1].strip()

    return {'time':time, 'performance':performance}


def read_crossvalidation_folder(Folder):

    # dictionary
    path = os.path.join('crossvalidations', Folder)
    array = {}
    for fname in os.listdir(path):
        if not fname.endswith('.result'): continue
        if '~' in fname: continue

        pos = tuple(map(int,fname.split('.')[0].split('x')))

        path = os.path.join('crossvalidations', Folder, fname)
        array[pos] = read_crossvalidation_file(path)

    return array
    
            
            
    
