



LowerBoundInputs = 1
UpperBoundInputs = 10
LowerBoundGates  = 1
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
UniquenessConstraint = True


import classifier

if __name__=="__main__":
    
    if 1:    
        # creates an image for each answer
        FnameCSV = "toy.csv"

        print
        print "Example for pilot:"
    
        parameters = {
            "FnameCSV":FnameCSV,
            "LowerBoundInputs":LowerBoundInputs,
            "UpperBoundInputs":UpperBoundInputs,
            "LowerBoundGates":LowerBoundGates,
            "UpperBoundGates":UpperBoundGates,
            "GateTypes":GateTypes,
            "EfficiencyConstraint":EfficiencyConstraint,
            "OptimizationStrategy":OptimizationStrategy,
            "BreakSymmetries":BreakSymmetries,
            "Silent":True,
            "UniquenessConstraint": UniquenessConstraint}

        answers = classifier.pilot(parameters)
        
        for i,x in enumerate(answers):
            FnamePDF = "toy_%i.pdf"%i
            classifier.gateinputs2pdf(FnamePDF, x, Silent=True)
            print " created", FnamePDF

        print " answers:", len(answers)
            
        
    if 0:
        # slices
        FnameCSV = "casestudies/C2_corrected.csv"

        print
        print "Example for slices (fixed number of inputs and gates):"
        print " Format: (Inputs, Gates, Answers)"
        hit = False
        for x in range(1,UpperBoundInputs+1):
            if hit: break
            for y in range(1, min(x+1,UpperBoundGates+1) ):
                if hit: break
                
                parameters = {
                    "FnameCSV":FnameCSV,

                    # slice:
                    "LowerBoundInputs": x,
                    "UpperBoundInputs": x,
                    "LowerBoundGates":  y,
                    "UpperBoundGates":  y,
                    
                    "GateTypes":GateTypes,
                    "EfficiencyConstraint":EfficiencyConstraint,
                    "OptimizationStrategy":OptimizationStrategy,
                    "BreakSymmetries":BreakSymmetries,
                    "Silent":True}

                answers = classifier.pilot(parameters)
                print "", x, y, len(answers)
                
                if answers: hit = True


        print "Answers:"
        for i,x in enumerate(answers):
            print " %i:"%i, x




















                
    
