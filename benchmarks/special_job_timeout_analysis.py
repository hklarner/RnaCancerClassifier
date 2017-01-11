

import sys
import os
import importlib

import networkx
import numpy
import random

import interfaces

def redo_problem(Folder, X, Y, TimeOut):

    FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, _ = Folder.split('_')
    DATASET = '_'.join([FROM,TO,SKIP,CLASSIFIER_ANNOTATION])


    path = 'datasets/{d}/{x}x{y}'.format(d=DATASET,x=X,y=Y)
    #print('working on {x}'.format(x=path))
    
    matrix, gateinputs = interfaces.files.read_dataset(path)

    fname_csv = 'tmp.csv'
    fname_asp = 'tmp.asp'

    
    interfaces.files.write_csvfile(fname_csv, matrix, gateinputs)
    interfaces.potassco.create_aspfile(FnameCSV  = fname_csv,
                                       FnameASP  = fname_asp,
                                       TemplateClassifier = CLASSIFIER_SOLUTION,
                                       TemplateObjective  = OBJECTIVE)

    time, solution = interfaces.potassco.timed_call_single_solution(fname_asp, TimeOut=TimeOut)
    
    os.remove(fname_csv)
    os.remove(fname_asp)

    #print('time: {x}'.format(x=time))
    print(time)

    return time
    
        
def run():

    Folder = "10x10_500x500_10x10_kobi_kobi_gates-inputs_10m"
    
    DataArray = interfaces.files.read_benchmark_folder(Folder)
    SampleRate = .1
    TimeOut = "60m"

    timeouts = DataArray.copy()
    
    for x in timeouts.keys():
        if not timeouts[x]["time"]==None:
            timeouts.pop(x)

    print("folder: {x}".format(x=Folder))
    print("new timeout: {x}".format(x=TimeOut))
    print("timeouts: {x}/{y}={z}".format(x=len(timeouts),y=len(DataArray),z=float(len(timeouts))/len(DataArray)))
    print("sample rate: {x}%".format(x=SampleRate*100))

    randomsample = random.sample(timeouts, int(SampleRate*len(timeouts)))

    for X,Y in randomsample:
        redo_problem(Folder, X, Y, TimeOut)
    


if __name__=="__main__":
    run()
