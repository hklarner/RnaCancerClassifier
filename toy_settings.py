


FnameCSV = "toy_data.csv"
FnameASP = "toy_classifier.asp"
UpperBoundInputs = 2
UpperBoundGates  = 2
GateTypes = [(1,0,1),(0,1,2)]
EfficiencyConstraint = True
OptimizationStrategy = 2

"""
User input explained:

 FnameCSV              = CSV data file (0/1 matrix, tissue samples = rows)
  Header               = ID, Annots, g1, g2, g3, ... (ID:sampleid, Annots:0=healthy/1=cancer, g1:0=low expression/1=high expression)
 FnameASP              = ASP filename that is generated
 UpperBoundInputs      = upper bound for total number of inputs for classifier
 UpperBoundGates       = upper bount for number of gates
 GateTypes             = a gate type is defined by (upper bound positive inputs, upper bound negative inputs , upper bound appearance of gate type)
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
    if 1 :
        classifier.csv2asp(
            FnameCSV,
            FnameASP,
            UpperBoundInputs,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy)
            
    if 1:
        GateInputs = "gate_input(1,negative,g1)"
        classifier.check_classifier(FnameCSV, GateInputs)

    if 1:
        GateInputs = "gate_input(2,positive,g2) gate_input(1,negative,g1)"
        FnamePDF = "toy_classifier.pdf"
        classifier.gateinputs2pdf(FnamePDF, GateInputs)

    
