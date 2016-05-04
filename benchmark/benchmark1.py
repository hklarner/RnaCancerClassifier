

import sys
sys.path = ["../"] + sys.path
import classifier


def run():
    FnameCSV = "benchmark1_tmp.csv"
    FnameASP = "benchmark1_tmp.asp"
    
    classifier.csv2asp( FnameCSV,
                        FnameASP,
                        UpperBoundInputs = 10,
                        UpperBoundGates  = 6,
                        GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":3,
                                      "LowerBoundNeg":0,"UpperBoundNeg":0,
                                      "UpperBoundOcc":2},
                                     {"LowerBoundPos":0,"UpperBoundPos":0,
                                      "LowerBoundNeg":0,"UpperBoundNeg":1,
                                      "UpperBoundOcc":4}],
                        EfficiencyConstraint = True,
                        OptimizationStrategy = 2,
                        Silent=True)

if __name__=="__main__":
    run()


