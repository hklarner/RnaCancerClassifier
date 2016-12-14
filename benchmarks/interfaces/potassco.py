

import os
import subprocess

import interfaces.templates

import sys
sys.path.insert(0, '../classifier')
import classifier as CLASSIFIER_SCRIPT


def create_aspfile(FnameCSV,FnameASP,TemplateClassifier,TemplateObjective):

    params_classifier = interfaces.templates.read_classifier(TemplateClassifier)
    params_objective  = interfaces.templates.read_objective(TemplateObjective)

    CLASSIFIER_SCRIPT.csv2asp(FnameCSV = FnameCSV,
                              FnameASP = FnameASP,
                              LowerBoundInputs = params_classifier['LowerBoundInputs'],
                              UpperBoundInputs = params_classifier['UpperBoundInputs'],
                              LowerBoundGates  = params_classifier['LowerBoundGates'],
                              UpperBoundGates  = params_classifier['UpperBoundGates'],
                              GateTypes        = params_classifier['GateTypes'],
                              
                              EfficiencyConstraint = params_objective['EfficiencyConstraint'],
                              OptimizationStrategy = params_objective['OptimizationStrategy'],
                              BreakSymmetries      = params_objective['BreakSymmetries'],
                              Silent               = True,
                              UniquenessConstraint = params_objective['UniquenessConstraint'],
                              PerfectClassifier    = params_objective['PerfectClassifier'],
                              UpperBoundFalsePos   = params_objective['UpperBoundFalsePos'],
                              UpperBoundFalseNeg   = params_objective['UpperBoundFalseNeg'])
    



def timed_call_single_solution(FnameASP, TimeOut):
    
    try:
        output = ''

        proc = subprocess.Popen(['interfaces/potassco_timeout.sh', TimeOut, FnameASP], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = proc.communicate()

    except Exception as Ex:
        print()
        print(output)
        print()
        print(Ex)
        print(' >> exception in potassco_timeout.sh')
        raise Ex

    if error:
        if '(clasp): INTERRUPTED by signal!' in error:
            return None, None
        else:
            print()
            print(output)
            print()
            print(error)
            print(' >> error in potassco_timeout.sh')
            raise Exception

    solution = output2gateids(output)

    if solution:
        # satisfiable
        solution = solution.pop()

    time = output2time(output)
    
    return time, solution


def output2time(Output):
    for line in Output.split('\n'):
        if line.startswith('CPU Time'):
            return line.split(':')[1].strip()
        
    
def output2gateids(Output):
    hit = False
    gateids = []
    for line in Output.split('\n'):

        if "gate_input" in line:
            if hit:
                print ">> ANSWER OVER SEVERAL LINES! REQURIES BUGFIX"
            else:
                hit = True
                gateids+=[line]
        elif "UNSATISFIABLE" in line:
            return None
        else:
            hit = False

    return gateids


