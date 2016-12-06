

import os

def read_pythonfile(Path):
    params = {}
    execfile(Path, params)
    
    return params


CLASSIFIER_KEYWORDS = ['LowerBoundInputs','UpperBoundInputs','LowerBoundGates','UpperBoundGates','GateTypes']

def read_classifier(Template):
    params = read_pythonfile(os.path.join('templates','classifiers',Template+'.py'))

    return dict((x,y) for x,y in params.items() if x in CLASSIFIER_KEYWORDS)


OBJECTIVE_KEYWORDS = ['EfficiencyConstraint','OptimizationStrategy','BreakSymmetries','UniquenessConstraint',
                      'PerfectClassifier','UpperBoundFalsePos','UpperBoundFalseNeg']

def read_objective(Template):
    params = read_pythonfile(os.path.join('templates','objectives',Template+'.py'))

    return dict((x,y) for x,y in params.items() if x in OBJECTIVE_KEYWORDS)


