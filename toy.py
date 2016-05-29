


FnameCSV = "toy.csv"
FnameASP = "toy.asp"
LowerBoundInputs = 0
UpperBoundInputs = 10
LowerBoundGates  = 0
UpperBoundGates  = 2
GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":2,
              "LowerBoundNeg":0,"UpperBoundNeg":0,
              "UpperBoundOcc":1},
             {"LowerBoundPos":0,"UpperBoundPos":0,
              "LowerBoundNeg":0,"UpperBoundNeg":1,
              "UpperBoundOcc":2}]
EfficiencyConstraint = False
OptimizationStrategy = 1
BreakSymmetries = True


import classifier

if __name__=="__main__":
    if 1:
        classifier.csv2asp(
            FnameCSV,
            FnameASP,
            LowerBoundInputs,
            UpperBoundInputs,
            LowerBoundGates,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy,
            BreakSymmetries)
            
    if 1:
        GateInputs = "gate_input(1,positive,g2) gate_input(2,positive,g3) gate_input(2,negative,g1)"
        classifier.check_classifier(FnameCSV, GateInputs)

    if 1:
        GateInputs = "gate_input(1,positive,g2) gate_input(2,positive,g3) gate_input(2,negative,g1)"
        FnamePDF = "toy.pdf"
        classifier.gateinputs2pdf(FnamePDF, GateInputs)
        
    if 0:
        FnameMAT = "toy.mat"
        Threshold = 250
        classifier.mat2csv(FnameMAT, Threshold)

    if 1:
        classifier.check_csv(FnameCSV)
        

    
