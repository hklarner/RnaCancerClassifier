


FnameCSV = "toy.csv"
FnameASP = "toy.asp"
UpperBoundInputs = 10
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
 OptimizationStrategy  = 0..4
   0 = no optimization
   1 = minimize number of gates, then minimize number of inputs
   2 = minimize number of inputs, then minimize number of gates
   3 = minimize number of inputs
   4 = minimize number of gates

 Note: a classifier is the conjunction of disjunctive gates (CNF)
"""


import classifier

if __name__=="__main__":
    if 1:
        parameters = {
            "FnameCSV":FnameCSV,
            "FnameASP":FnameASP,
            "UpperBoundInputs":UpperBoundInputs,
            "UpperBoundGates":UpperBoundGates,
            "GateTypes":GateTypes,
            "EfficiencyConstraint":EfficiencyConstraint,
            "OptimizationStrategy":OptimizationStrategy,
            "BreakSymmetries":BreakSymmetries,
            "Silent":True}

        answers = classifier.pilot(parameters)
        
        for i,x in enumerate(answers):
            FnamePDF = "answer%i.pdf"%i
            classifier.gateinputs2pdf(FnamePDF, x, Silent=True)
            print "created", FnamePDF

        print "answers:", len(answers)
            
        

    
