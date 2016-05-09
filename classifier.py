# -*- coding: utf-8 -*-



import csv
import subprocess
from scipy.io import loadmat
import numpy as np



"""
User input explained:

 FnameCSV              = CSV data file (0/1 matrix, tissue samples = rows)
  Header               = ID, Annots, g1, g2, g3, ... (ID:sampleid, Annots:0=healthy/1=cancer, g1:0=low expression/1=high expression)
 FnameASP              = ASP filename that is generated
 UpperBoundInputs      = upper bound for total number of inputs for classifier
 UpperBoundGates       = upper bound for number of gates
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


OptimizationStrategyMapping = {1:"minimize inputs then minimize gates",
                               2:"minimize gates then minimize inputs",
                               3:"minimize inputs",
                               4:"minimize gates"}

def csv2asp(FnameCSV,
            FnameASP,
            UpperBoundInputs,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy,
            Silent=False
            ):

    if not Silent:
        print "\n--- csv2asp"
        print " input file:", FnameCSV
        print " upper bound on inputs:", UpperBoundInputs
        print " upper bound on gates:", UpperBoundGates
        print " gate types:", GateTypes
        print " efficiency constraints:",EfficiencyConstraint
        print " optimization strategy:",OptimizationStrategy, "(%s)"%OptimizationStrategyMapping[OptimizationStrategy]
    

    with open(FnameCSV, 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.next()
        header = [x.strip() for x in header]
        miRNAs = [x for x in header if not x in ["ID", "Annots"]]
        rows = [dict(zip(header,[y.strip() for y in x])) for x in reader]

        if not Silent:
            print " miRNAs: ", len(miRNAs)
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
        datafile+= ["%%  gate types: %s"%str(GateTypes)]
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
                    "is_mirna(Y) :- data(X,Y,Z).",
                    ""]

    datafile+= ['']
    datafile+= ['']
    datafile+= ['%%%% Classifier Structure %%%%']
    datafile+= ["% definition of gate types in terms of upper bounds on number of inputs"]

    for x, gate_type in enumerate(GateTypes):
        datafile+= ["is_gate_type(type%i)."%(x+1)]
        datafile+= ["upper_bound_pos_inputs(type%i, %i)."%(x+1,gate_type["UpperBoundPos"])]
        datafile+= ["upper_bound_neg_inputs(type%i, %i)."%(x+1,gate_type["UpperBoundNeg"])]
        datafile+= ["lower_bound_pos_inputs(type%i, %i)."%(x+1,gate_type["LowerBoundPos"])]
        datafile+= ["lower_bound_neg_inputs(type%i, %i)."%(x+1,gate_type["LowerBoundNeg"])]
        datafile+= ["upper_bound_gate_occurence(type%i, %i)."%(x+1,gate_type["UpperBoundOcc"])]
        datafile+= ['']

    datafile+= ['']
    datafile+= ["% each input may be positive or negative"]
    datafile+= ['is_sign(positive). is_sign(negative).']
    datafile+= [""]
    datafile+= ["% upper bound for total number of inputs"]
    datafile+= ['upper_bound_inputs(%i).'%UpperBoundInputs]
        
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
        datafile+= ['feasible_pos_miRNA(MiRNA) :- is_mirna(MiRNA), data(TissueID, MiRNA, high), tissue(TissueID,cancer).']
        datafile+= ['feasible_neg_miRNA(MiRNA) :- is_mirna(MiRNA), data(TissueID, MiRNA, low),  tissue(TissueID,cancer).']

        datafile+= ['']
        datafile+= ['% Third decision: each gate is assigned a number of inputs']
        datafile+= ['X {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).']
        datafile+= ['X {gate_input(GateID, negative, MiRNA): feasible_neg_miRNA(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).']
        
    else:
        datafile+= ['% efficiency OFF: unrestricted miRNAs for inputs']
        datafile+= ['']
        datafile+= ['% Third decision: each gate is assigned a number of inputs']
        datafile+= ['X {gate_input(GateID, positive, MiRNA): is_mirna(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).']
        datafile+= ['X {gate_input(GateID, negative, MiRNA): is_mirna(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).']        
        
    
    datafile+= ['']
    datafile+= ['']
    datafile+= ['%%%% Constraints %%%%']
    datafile+= ['% each gate must have at least one input']
    datafile+= ['1 {gate_input(GateID, Sign, MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).']

    datafile+= ['']
    datafile+= ['% inputs must be unique for a classifer']
    datafile+= ["{gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_gate_id(GateID)} 1 :- is_mirna(MiRNA)."]
    
    datafile+= ['']
    datafile+= ['% the total number of inputs is bounded']
    datafile+= ['{gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} X :- upper_bound_inputs(X).']
        
    datafile+= ['']
    datafile+= ['% the number of occurences of a gate type is bounded']
    datafile+= ['{gate_type(GateID,GateType): is_gate_id(GateID)} X :- is_gate_type(GateType), upper_bound_gate_occurence(GateType,X).']

    datafile+= ['']
    datafile+= ['% gates are disjunctive (one active input suffices to activate gate)']
    datafile+= ["gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high)."]
    datafile+= ["gate_fires(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low)."]

    datafile+= ['']
    datafile+= ['% the classifier is a conjunction of all gate evaluations.']
    datafile+= ["classifier(TissueID,healthy) :- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID)."]
    datafile+= ["classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID)."]

    datafile+= ['']
    datafile+= ["% the classifier must agree with the tissue data."]
    datafile+= [":- tissue(TissueID,healthy), classifier(TissueID,cancer)."]
    datafile+= [":- tissue(TissueID,cancer),  classifier(TissueID,healthy)."]
    
    datafile+= ['']
    if OptimizationStrategy==1:
        datafile+= ["% optimization setup 2: first number of inputs then number of gates."]
        datafile+= ["#minimize{ 1@1,MiRNA: gate_input(GateID,Sign,MiRNA) }."]
        datafile+= ["#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==2:
        datafile+= ["% optimization setup 1: first number of gates then number of inputs."]
        datafile+= ["#minimize{ 1@1,GateID:gate_input(GateID,Sign,MiRNA) }."]
        datafile+= ["#minimize{ 1@2,MiRNA: gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==3:
        datafile+= ["% optimization setup 3: only number of inputs."]
        datafile+= ["#minimize{ 1,MiRNA:gate_input(GateID,Sign,MiRNA) }."]
        
    elif OptimizationStrategy==4:
        datafile+= ["% optimization setup 4: only number of gates."]
        datafile+= ["#minimize{ 1,GateID:gate_input(GateID,Sign,MiRNA) }."]
           
    
    datafile+= ['']
    datafile+= ["#show gate_input/3."]
    
    with open(FnameASP, 'w') as f:
       f.writelines("\n".join(datafile))

    if not Silent:
        print " created:", FnameASP
        print " now run: gringo %s | clasp --opt-mode=optN --quiet=1"%FnameASP


def gateinputs2pdf(FnamePDF, GateInputs):
    """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """
    print "\n--- gateinputs2pdf"

    GateInputs = GateInputs.strip()
    GateInputs = GateInputs.split()
    print " found %i inputs:"%len(GateInputs),GateInputs
    
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
    print " created", FnamePDF


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
    print " found %i input(s) for function generation:"%len(GateInputs),GateInputs
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
    print "\n--- check_classifier"

    
    hits = set([])
    with open(FnameCSV, 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.next()
        header = [x.strip() for x in header]
        miRNAs = [x for x in header if not x in ["ID", "Annots"]]
        rows = [dict(zip(header,[y.strip() for y in x])) for x in reader]

        print " miRNAs: ", len(miRNAs)
        print " samples:", len(rows)

        function = gateinputs2function(GateInputs)
        print " testing each sample against the function.."
        for x in rows:
            malfunction = function(x)
            if malfunction:
                hits.add(x["ID"])
                for location in malfunction:
                    print " ** found malfunction:"
                    for item in sorted(location.items()):
                        print "    %s = %s"%item
                    

    print " classifier =",GateInputs
    print " data =",FnameCSV
    if hits:
        print " result = %i inconsistencies"%(len(hits)), hits
    else:
        print " result = classifier and data are consistent"
        
        
       
       
       
def mat2csv(FnameMAT, Threshold):
	"""
   Threshold for binarization (0 if variable<250 else 1):
   use 250 for toy.mat files
   """
	print "\n--- mat2csv"
   # Read .mat file
	datafile = loadmat(FnameMAT)
	print " input file: "+str(FnameMAT)

	col = datafile['SimDataHeike']['Values'][0,0][0,:]
	row = datafile['SimDataHeike']['Values'][0,0][:,0]
	print " samples: "+str(col.size)
	print " miRNAs: "+str(row.size)

	# ID column
	id_column = []
	id_column.append("ID")
	for i in range(0,col.size):
		id = i
		id_column.append(i+1)

	# Write .csv file
	np.savetxt(str(FnameMAT[:-4])+'_binary.csv', 
          	 id_column, 
          	 delimiter=',', 
          	 fmt='%s')
           
	# Annots column
	annots_column = []
	annots_column.append("Annots")
	cancer_count = 0
	for c in range(0,col.size):
		variable = datafile['SimDataHeike']['Annots'][0,0][0,c]
		annots_column.append(variable)
		if variable == 1:
			cancer_count=cancer_count+1
	print " cancer cells: "+str(cancer_count)
	
	oldfile = open(str(FnameMAT[:-4])+'_binary.csv')
	olddata = [item for item in csv.reader(oldfile)]
	oldfile.close()    

	newdata = []
 
	for i, item in enumerate(olddata):
    		try:
      	 		item.append(annots_column[i])
    		except IndexError, e:
       	 		item.append("placeholder")
    		newdata.append(item)
 
	newfile = open(str(FnameMAT[:-4])+'_binary.csv', 'w')
	csv.writer(newfile).writerows(newdata)
	newfile.close()
	
	# Values of miRNAs in columns            
	# First row to end
	for r in range(0,row.size):      
           
		oldfile = open(str(FnameMAT[:-4])+'_binary.csv')
		olddata = [item for item in csv.reader(oldfile)]
		oldfile.close()    
      
		newcolumn = []
		newcolumn.append("g"+str(r+1))
		for c in range(0,col.size):
				variable = datafile['SimDataHeike']['Values'][0,0][r,c]
				binary = 0 if variable<250 else 1
				newcolumn.append(binary)
 
				newdata = []
 
		for i, item in enumerate(olddata):
    			try:
       				item.append(newcolumn[i])
    			except IndexError, e:
        				item.append("placeholder")
    			newdata.append(item)
 
		newfile = open(str(FnameMAT[:-4])+'_binary.csv', 'w')
		csv.writer(newfile).writerows(newdata)
		newfile.close()
	
	# Get classifier
	print " classifier: "
	for c in range(0,6):
		input = datafile['SimDataHeike']['Synthesis_Function'][0,0][0,c]
		for r in range(0,3):
			if input[r] > 0:
				print "   gate_input("+str(c+1)+",positive,"+str(input[r])+")"
			if input[r] < 0:
				nosign = input[r]*-1
				print "   gate_input("+str(c+1)+",negative,"+str(nosign)+")"
				
	print " created: "+str(FnameMAT[:-4])+"_binary.csv"


 
 
 
 

if __name__=="__main__":
    print "nothing to do"
