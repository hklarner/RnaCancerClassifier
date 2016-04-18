# -*- coding: utf-8 -*-



import csv
import subprocess



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


OptimizationStrategyMapping = {1:"minimize gates then minimize inputs",
                               2:"minimize inputs then minimize gates",
                               3:"minimize inputs",
                               4:"minimize gates"}

def csv2asp(FnameCSV,
        FnameASP,
        UpperBoundInputs,
        UpperBoundGates,
        GateTypes,
        EfficiencyConstraint,
        OptimizationStrategy):

    print "Input File:", FnameCSV
    print " upper bound on inputs:", UpperBoundInputs
    print " upper bound on gates:", UpperBoundGates
    print " gate types (upper bound positive / negative inputs):", GateTypes
    print " efficiency constraints:",EfficiencyConstraint
    print " optimization strategy:",OptimizationStrategy, "(%s)"%OptimizationStrategyMapping[OptimizationStrategy]
    print " Note: a classifier is the conjunction of disjunctive gates (CNF)"
    

    with open(FnameCSV, 'rb') as f:
        reader = csv.reader(f)
        
        header = reader.next()
        miRNAs = [x for x in header if not x in ["ID", "Annots"]]
        print " miRNAs: ", len(miRNAs)
        
        rows = [dict(zip(header,x)) for x in reader]
        print " samples:", len(rows)

        datafile = [""]
        datafile+= ["% ASP constraints for computing a classifier (in this case a Boolean Function),"]
        datafile+= ["% that agrees with given tissue data (either cancerous or healthy) and"]
        datafile+= ["% and satisfies certain structural constraints."]
        datafile+= ["% Note: a classifier is the conjunction of disjunctive gates (CNF)"]
        datafile+= ["% written by K. Becker and H. Klarner, March 2016, FU Berlin."]
        datafile+= [""]
        datafile+= ["%% InputFile = %s"%FnameCSV]
        datafile+= ["%%  upper bound on inputs: %i"%UpperBoundInputs]
        datafile+= ["%%  upper bound on gates: %i"%UpperBoundGates]
        datafile+= ["%%  gate types (upper bound positive / negative inputs): %s"%str(GateTypes)]
        datafile+= ["%%  efficiency constraints: %s"%str(EfficiencyConstraint)]
        datafile+= ["%%  optimization strategy: %i  (%s)"%(OptimizationStrategy,OptimizationStrategyMapping[OptimizationStrategy])]
        datafile+= [""]
                    
        datafile+= ['% the tissue data, a tissue ID followed by either "cancer" or "healthy"']
        dummy = []
        for x in rows:
            y = "healthy" if x["Annots"]=="0" else "cancer"
            dummy.append( "tissue(%s,%s)."%(x["ID"],y) )
            if sum(map(len,dummy))>100:
                datafile+= [" ".join(dummy)]
                dummy = []
                    
        datafile+= [" ".join(dummy)]
        datafile+= [""]

        datafile+= ['% for binding variables we need the "is_tissue_id" predicate',
                    "is_tissue_id(X) :- tissue(X,Y).",
                    ""]

        datafile+= ['% the miRNA data, a tissue ID and miRNA ID followed by either "high" or "low"']
        dummy = []
        for x in rows:
            for miRNA in miRNAs:
                y = "high" if x[miRNA]=="1" else "low"
                dummy.append("data(%s,%s,%s)."%(x["ID"],miRNA,y))
                if sum(map(len,dummy))>100:
                    datafile+= [" ".join(dummy)]
                    dummy = []
                    
        datafile+= [" ".join(dummy)]
        datafile+= [""]

        datafile+= ['% for binding variables we need the "is_miRNA" predicate',
                    "is_miRNA(Y) :- data(X,Y,Z).",
                    ""]

    datafile+= ['']
    datafile+= ['']
    datafile+= ['%%%% Classifier Structure %%%%']
    datafile+= ["% definition of gate types in terms of upper bounds on number of inputs"]
    datafile+= ["is_gate_type(1..%i)."%len(GateTypes)]

    for x, gate_type in enumerate(GateTypes):
        ub_pos, ub_neg = gate_type
        datafile+= ["upper_bound_pos_inputs(%i, %i). %% GateType=%i"%(x+1,ub_pos,x+1)]
        datafile+= ["upper_bound_neg_inputs(%i, %i). %% GateType=%i"%(x+1,ub_neg,x+1)]
        

    datafile+= [""]
    datafile+= ["% each input may be positive or negative"]
    datafile+= ['is_sign(positive). is_sign(negative).']
    datafile+= [""]
    datafile+= ["% upper bound for total number of inputs"]
    datafile+= ['upper_bound_total_inputs(%i).'%UpperBoundInputs]
        
    datafile+= ['']
    datafile+= ['']
    datafile+= ['%%%% Decisions %%%%']
    datafile+= ['% First decision: the exact number of gates']
    datafile+= ['1 {number_of_gates(1..%i)} 1.'%UpperBoundGates]
    datafile+= ['is_integer(1..%i).'%UpperBoundGates]
    datafile+= ['is_gate_id(GateID) :- number_of_gates(X), is_integer(GateID), GateID<=X.']
    datafile+= ['']
    datafile+= ['% Second decision: each gates is assigned a gate type']
    datafile+= ['1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).']
    datafile+= ['']

    if EfficiencyConstraint:
        datafile+= ['% efficiency ON: restrict miRNA for inputs (requires the assumptionin that number of miRNAs is minimal)']
        datafile+= ['feasible_pos_miRNA(MiRNA) :- is_miRNA(MiRNA), data(TissueID, MiRNA, high), tissue(TissueID,cancer).']
        datafile+= ['feasible_neg_miRNA(MiRNA) :- is_miRNA(MiRNA), data(TissueID, MiRNA, low),  tissue(TissueID,cancer).']

        datafile+= ['']
        datafile+= ['% Third decision: each gate is assigned a number of inputs']
        datafile+= ['0 {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} X :- is_gate_id(GateID), gate_type(GateID, GateType), upper_bound_pos_inputs(GateType, X).']
        datafile+= ['0 {gate_input(GateID, negative, MiRNA): feasible_neg_miRNA(MiRNA)} X :- is_gate_id(GateID), gate_type(GateID, GateType), upper_bound_neg_inputs(GateType, X).']
        
    else:
        datafile+= ['% efficiency OFF: unrestricted miRNAs for inputs']
        datafile+= ['']
        datafile+= ['% Third decision: each gate is assigned a number of inputs']
        datafile+= ['0 {gate_input(GateID, positive, MiRNA): is_miRNA(MiRNA)} X :- is_gate_id(GateID), gate_type(GateID, GateType), upper_bound_pos_inputs(GateType, X).']
        datafile+= ['0 {gate_input(GateID, negative, MiRNA): is_miRNA(MiRNA)} X :- is_gate_id(GateID), gate_type(GateID, GateType), upper_bound_neg_inputs(GateType, X).']        
        
    
    datafile+= ['']
    datafile+= ['']
    datafile+= ['%%%% Constraints %%%%']
    datafile+= ['% each gate must have at least one input']
    datafile+= ['1 {gate_input(GateID, Sign, MiRNA): is_sign(Sign), is_miRNA(MiRNA)} :- is_gate_id(GateID).']
    
    datafile+= ['']
    datafile+= ['% the total number of inputs is bounded']
    datafile+= ['{gate_input(GateID, Sign, MiRNA): is_gate_id(GateID), is_sign(Sign), is_miRNA(MiRNA)} X :- upper_bound_total_inputs(X).']
    
    datafile+= ['']
    datafile+= ['% gates are disjunctive (one active input suffices to activate gate)']
    datafile+= ["gate_evaluation(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high)."]
    datafile+= ["gate_evaluation(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low)."]

    datafile+= ['']
    datafile+= ['% inputs must not be positive and negative in the same gate']
    datafile+= [":- gate_input(GateID,positive,MiRNA), gate_input(GateID,negative,MiRNA)."]
    datafile+= ['']
    
    datafile+= ['% an input cannot be used for two different gates']
    datafile+= [":- gate_input(X,_,MiRNA), gate_input(Y,_,MiRNA), X<Y."]
    datafile+= [""]

    datafile+= ['% the classifier is a conjunction of all gate evaluations.']
    datafile+= ["classifier(TissueID, healthy) :- not gate_evaluation(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID)."]
    datafile+= ["classifier(TissueID, cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID)."]
    datafile+= [""]

    datafile+= ["% the classifier mus agree with the tissue data."]
    datafile+= [":- tissue(TissueID,healthy), classifier(TissueID,cancer)."]
    datafile+= [":- tissue(TissueID,cancer),  classifier(TissueID,healthy)."]
    datafile+= [""]
    
    if OptimizationStrategy==1:
        datafile+= ["% optimization setup 1: first number of gates then number of inputs."]
        datafile+= ["#minimize{ 1@1,GateID:gate_input(GateID,Sign,MiRNA) }."]
        datafile+= ["#minimize{ 1@2,MiRNA: gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==2:
        datafile+= ["% optimization setup 2: first number of inputs then number of gates."]
        datafile+= ["#minimize{ 1@1,MiRNA: gate_input(GateID,Sign,MiRNA) }."]
        datafile+= ["#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==3:
        datafile+= ["% optimization setup 3: only number of inputs."]
        datafile+= ["#minimize{ 1,MiRNA:gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==4:
        datafile+= ["% optimization setup 4: only number of gates."]
        datafile+= ["#minimize{ 1,GateID:gate_input(GateID,Sign,MiRNA) }."]
           
    
    datafile+= [""]
    datafile+= ["#show gate_input/3."]
    
    with open(FnameASP, 'w') as f:
       f.writelines("\n".join(datafile))

    print "Created:", FnameASP
    print "To execute run: gringo %s | clasp --opt-mode=optN"%FnameASP


def gateinputs2pdf(GateInputs, FnamePDF):
    """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """

    GateInputs = GateInputs.strip()
    GateInputs = GateInputs.split()
    print "found % inputs:"%len(GateInputs),GateInputs
    GateInputs = [x[x.find("(")+1:-1].split(",") for x in GateInputs]


    s = ['digraph "classifier" {']
    s+= ['node [color="none", style="filled", shape="rect", fillcolor="gray95"];']

    gates = set([])
    for gate, sign, mrna in GateInputs:
        gates.add(gate)
        if sign=="positive":
            arrow="normal"
            color="black"
        else:
            arrow="tee"
            color="red"
            
        s+= ['"%s" -> "gate%s" [arrowhead="%s", color="%s"];'%(mrna,gate,arrow,color)]

    for gate in gates:
        s+= ['"gate%s" -> "classifier" [arrowhead="normal", color="black"];'%gate]
    s+= ['}']


    cmd = ["dot", "-Tpdf", "-o", FnamePDF]
    dotfile = "\n".join(s)
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate( input=dotfile )
    proc.stdin.close()


def gateinputs2function(GateInputs):
    example = """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """

    if "." in GateInputs:
        print 'removing dots (".") from GateInputs'
        GateInputs = GateInputs.replace(".","")
    if ", " in GateInputs or " ," in GateInputs:
        print "remove spaces inside of gate_input predecates."
        print example
        raise Exception

    GateInputs = GateInputs.strip()
    GateInputs = GateInputs.split()
    print "found %i inputs:"%len(GateInputs),GateInputs
    GateInputs = [x[x.find("(")+1:-1].split(",") for x in GateInputs]

    seen = set([])
    Gates = {}
    for id, sign, rna in GateInputs:
        if rna in seen:
            print "miRNA %s appears several times in GateInputs!"%rna
        if not id in Gates:
            Gates[id] = set([])

        Gates[id].add((rna,sign))
        seen.add(rna)
            
        
    def function(SampleDict):
        malfunction = []
        classifier_fires = True
        for gateid, inputs in Gates.items():
            gate_fires = False
            rnas = set([])
            for rna, sign in inputs:
                rnas.add(rna)
                if sign=="positive" and SampleDict[rna]=="1":
                    gate_fires = True
                elif sign=="negative" and SampleDict[rna]=="0":
                    gate_fires = True
                    
            if SampleDict["Annots"] == "1" and not gate_fires:
                malfunction+= [{"tissue":"cancer",
                                "tissue_id":SampleDict["ID"],
                                "gate_id":gateid,
                                "gate_inputs":inputs,
                                "miRNA_expressions":",".join(["%s=%s"%item for item in SampleDict.items() if item[0] in rnas])}]

            if SampleDict["Annots"] == "0" and gate_fires:
                malfunction+= [{"tissue":"healthy",
                                "tissue_id":SampleDict["ID"],
                                "gate_id":gateid,
                                "gate_inputs":inputs,
                                "miRNA_expressions":",".join(["%s=%s"%item for item in SampleDict.items() if item[0] in rnas])}]

            classifier_fires = classifier_fires and gate_fires

        if SampleDict["Annots"] == "0" and not classifier_fires:
            malfunction = []
            
        return malfunction

    return function
                        
        
        

    

def check_classifier(FnameCSV, GateInputs):
    """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """

    
    hits = set([])
    with open(FnameCSV, 'rb') as f:
        reader = csv.reader(f)
        
        header = reader.next()
        miRNAs = [x for x in header if not x in ["ID", "Annots"]]
        print " miRNAs: ", len(miRNAs)
        
        samples = [dict(zip(header,x)) for x in reader]
        print " samples:", len(samples)

        function = gateinputs2function(GateInputs)
        for x in samples:
            malfunction = function(x)
            if malfunction:
                hits.add(x["ID"])
                for location in malfunction:
                    print "-- found malfunction:"
                    for item in sorted(location.items()):
                        print " %s=%s"%item
                    

    print "classifier=",GateInputs
    print "data=",FnameCSV
    if hits:
        print "result= %i inconsistencies"%(len(hits)), hits
    else:
        print "result= classifier and data are consistent"



        

if __name__=="__main__":
    print "nothing to do"
