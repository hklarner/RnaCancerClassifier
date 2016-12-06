


FnameCSV = "C2.csv"
FnameASP = "C2.asp"
LowerBoundInputs = 0
UpperBoundInputs = 10
LowerBoundGates  = 1
UpperBoundGates  = 6
GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":3,
              "LowerBoundNeg":0,"UpperBoundNeg":0,
              "UpperBoundOcc":2},
             {"LowerBoundPos":0,"UpperBoundPos":0,
              "LowerBoundNeg":0,"UpperBoundNeg":1,
              "UpperBoundOcc":4}]
EfficiencyConstraint = True
OptimizationStrategy = 1
BreakSymmetries = True
UniquenessConstraint = True
Silent = False
PerfectClassifier = True
UpperBoundFalsePos = 0
UpperBoundFalseNeg = 0


import sys
sys.path = ["../"] + sys.path
import classifier

if __name__=="__main__":
    if 0 :
        classifier.check_csv(FnameCSV)
        
        classifier.csv2asp(FnameCSV,
            FnameASP,
            LowerBoundInputs,
            UpperBoundInputs,
            LowerBoundGates,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy,
            BreakSymmetries,
            Silent,
            UniquenessConstraint,
	    PerfectClassifier,
	    UpperBoundFalsePos,
	    UpperBoundFalseNeg
            )
            
    if 1 :
        # basel classifier
        GateInputs = "gate_input(1,negative,g7) gate_input(2,negative,g6) gate_input(3,negative,g4) gate_input(4,negative,g3) "
        GateInputs+= "gate_input(5,positive,g1) gate_input(5,positive,g2) gate_input(5,positive,g8) "
        GateInputs+= "gate_input(6,positive,g1) gate_input(6,positive,g5) gate_input(6,positive,g8)"
        classifier.check_classifier(FnameCSV, GateInputs)

    if 0 :
        # without Kobi's constraints
        GateInputs = "gate_input(2,positive,g41) gate_input(1,negative,g4) gate_input(1,negative,g13) gate_input(1,negative,g34) gate_input(2,negative,g3) gate_input(2,negative,g18)"

        FnamePDF = "C2_classifier_without_kobi.pdf"
        classifier.gateinputs2pdf(FnamePDF, GateInputs)
        
        
    if 0 : 
    	  FnameMAT = "casestudy01.mat"
    	  Threshold = 250
    	  classifier.mat2csv(FnameMAT, Threshold)

    
