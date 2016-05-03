


FnameCSV = "casestudy01.csv"
FnameASP = "casestudy01.asp"
UpperBoundInputs = 10
UpperBoundGates  = 6
GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":3,
              "LowerBoundNeg":0,"UpperBoundNeg":0,
              "UpperBoundOcc":2},
             {"LowerBoundPos":0,"UpperBoundPos":0,
              "LowerBoundNeg":0,"UpperBoundNeg":1,
              "UpperBoundOcc":4}]
EfficiencyConstraint = True
OptimizationStrategy = 2

"""
User input explained:

 FnameCSV              = CSV data file (0/1 matrix, tissue samples = rows)
  Header               = ID, Annots, g1, g2, g3, ... (ID:sampleid, Annots:0=healthy/1=cancer, g1:0=low expression/1=high expression)
 FnameASP              = ASP filename that is generated
 UpperBoundInputs      = upper bound for total number of inputs for classifier
 UpperBoundGates       = upper bount for number of gates
 GateTypes             = a gate type is defined in terms of
   LowerBoundPos = lower bound of positive inputs to gate
   UpperBoundPos = upper bound of positive inputs to gate
   LowerBoundNeg = lower bound of negative inputs to gate
   UpperBoundNeg = upper bound of negative inputs to gate
   UpperBoundOcc = upper bound of occurences of gate in classifier
 EfficiencyConstraint  = Katinka's efficiency constraints: positive (negative) inputs must be highly (lowly) expressed on some cancer tissue
 OptimizationStrategy  = 1..4
   1 = minimize number of gates, then minimize number of inputs
   2 = minimize number of inputs, then minimize number of gates
   3 = minimize number of inputs
   4 = minimize number of gates

 Note: a classifier is the conjunction of disjunctive gates (CNF)
"""

import sys
sys.path = ["../"] + sys.path
import classifier

if __name__=="__main__":
    if 1 :
        classifier.csv2asp(
            FnameCSV,
            FnameASP,
            UpperBoundInputs,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy)
            
    if 0 :
        GateInputs = "gate_input(1,negative,g1)"
        classifier.check_classifier(FnameCSV, GateInputs)

    if 0 :
        GateInputs = "gate_input(2,positive,g2) gate_input(1,negative,g1)"
        FnamePDF = "toy_classifier.pdf"
        classifier.gateinputs2pdf(FnamePDF, GateInputs)
        
    if 0 : 
    	  FnameMAT = "casestudy01.mat"
    	  Threshold = 250
    	  classifier.mat2csv(FnameMAT, Threshold)

    
