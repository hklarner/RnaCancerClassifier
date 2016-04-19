


FnameCSV = "example.csv"
FnameASP = "exmaple.asp"
UpperBoundInputs = 4
UpperBoundGates  = 2
GateTypes = [(2,0),]
EfficiencyConstraint = True
OptimizationStrategy = 1

"""
User input explained:

 FnameCSV              = CSV data file (0/1 matrix, tissue samples = rows)
  Header               = ID, Annots, g1, g2, g3, ... (ID:sampleid, Annots:0=healthy/1=cancer, g1:0=low expression/1=high expression)
 FnameASP              = ASP filename that is generated
 UpperBoundInputs      = upper bound for total number of inputs for classifier
 UpperBoundGates       = upper bount for number of gates
 GateTypes             = a gate type is defined by the upper bounds for its positive / negative inputs
 EfficiencyConstraint  = Katinka's efficiency constraints: positive (negative) inputs must be highly (lowly) expressed on some cancer tissue
 OptimizationStrategy  = 1..4
   1 = minimize number of gates, then minimize number of inputs
   2 = minimize number of inputs, then minimize number of gates
   3 = minimize number of inputs
   4 = minimize number of gates

 Note: a classifier is the conjunction of disjunctive gates (CNF)
"""


import classifier

if __name__=="__main__":
    if 0 :
        classifier.csv2asp(
            FnameCSV,
            FnameASP,
            UpperBoundInputs,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy)
            
    classifier.check_classifier(FnameCSV, GateInputs)

    
