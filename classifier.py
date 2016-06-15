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
 LowerBoundInputs      = lower bound for total number of inputs for classifier
 UpperBoundInputs      = upper bound for total number of inputs for classifier
 LowerBoundGates       = lower bound for number of gates
 UpperBoundGates       = upper bound for number of gates
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
 BreakSymmetries       = whether you want to break gate_id and gate_input symmetries (warning: expensive)

 Note: a classifier is the conjunction of disjunctive gates (CNF)
"""


OptimizationStrategyMapping = {0:"no optimization",
                               1:"minimize inputs then minimize gates",
                               2:"minimize gates then minimize inputs",
                               3:"minimize inputs",
                               4:"minimize gates"}


def csv2rows(FnameCSV):
    """
    Converts a csv file to a list of dictionaries.
    """

    with open(FnameCSV, 'rb') as f:
        reader = csv.reader(f, delimiter=",")
        for x in reader:
            if not x:continue
            header = x
            header = [x.strip() for x in header]
            break
        
        miRNAs = [x for x in header if not x in ["ID", "Annots"]]

        IDs = set([])
        rows = []
        for x in reader:
            if not x: continue
            if not x[0].strip(): continue
            newrow = dict(zip(header,[y.strip() for y in x]))
            if newrow["ID"] in IDs:
                print "\n***ERROR: row IDs must be unique, found duplicate (%s)."%newrow["ID"]
                raise Exception
            IDs.add(newrow["ID"])
            rows.append(newrow)

    return miRNAs, rows

    
def csv2asp(FnameCSV,
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
            ):

    if not Silent:
        print "\n--- csv2asp"
        print " input file:", FnameCSV
        print " upper bound on inputs:", UpperBoundInputs
        print " upper bound on gates:", UpperBoundGates
        print " gate types:", GateTypes
        print " efficiency constraints:",EfficiencyConstraint
        print " optimization strategy:",OptimizationStrategy, "(%s)"%OptimizationStrategyMapping[OptimizationStrategy]

    assert(LowerBoundGates>0)
    
    miRNAs, rows = csv2rows(FnameCSV)

    if not Silent:
        print " miRNAs: ", len(miRNAs)
        print " samples:", len(rows)

    datafile = ['']
    datafile+= ['% ASP constraints for computing a miRNA cancer classifier']
    datafile+= ['% that agrees with given tissue data and satisfies given structural constraints.']
    datafile+= ['% note: A classifier is a Boolean expression in conjunctive form.']
    datafile+= ['% the homepage of the project is https://github.com/hklarner/RnaCancerClassifier.']
    datafile+= ['% written by K. Becker and H. Klarner, March 2016, FU Berlin.']
    datafile+= ['']
    datafile+= ['%% InputFile = %s'%FnameCSV]
    datafile+= ['%%  efficiency constraints: %s'%str(EfficiencyConstraint)]
    datafile+= ['%%  optimization strategy: %i  (%s)'%(OptimizationStrategy,OptimizationStrategyMapping[OptimizationStrategy])]
    datafile+= ['']
    datafile+= ['']
                
    datafile+= ['%%% The tissue data']
    dummy = []
    for x in rows:
        y = "healthy" if x["Annots"]=="0" else "cancer"
        dummy.append( "tissue(%s,%s)."%(x["ID"],y) )
        if sum(map(len,dummy))>100:
            datafile+= [" ".join(dummy)]
            dummy = []
                
    datafile+= [" ".join(dummy)]
    datafile+= [""]
    datafile+= ['%%% The miRNA data']
    dummy = []
    for x in rows:
        for miRNA in miRNAs:
            y = "high" if x[miRNA]=="1" else "low"
            dummy.append("data(%s,%s,%s)."%(x["ID"],miRNA,y))
            if sum(map(len,dummy))>100:
                datafile+= [" ".join(dummy)]
                dummy = []
                
    datafile+= [' '.join(dummy)]
    datafile+= ['']
    datafile+= ['']
    
    datafile+= ["%%% User Input"]
    datafile+= ['lower_bound_inputs(%i).'%LowerBoundInputs]
    datafile+= ['upper_bound_inputs(%i).'%UpperBoundInputs]
    datafile+= ['lower_bound_gates(%i).'%LowerBoundGates]
    datafile+= ['upper_bound_gates(%i).'%UpperBoundGates]
    datafile+= ['']

    for x, gate_type in enumerate(GateTypes):
        datafile+= ["%% gate type %i."%(x+1)]
        datafile+= ["is_gate_type(%i)."%(x+1)]
        datafile+= ["upper_bound_pos_inputs(%i, %i)."%(x+1,gate_type["UpperBoundPos"])]
        datafile+= ["upper_bound_neg_inputs(%i, %i)."%(x+1,gate_type["UpperBoundNeg"])]
        datafile+= ["lower_bound_pos_inputs(%i, %i)."%(x+1,gate_type["LowerBoundPos"])]
        datafile+= ["lower_bound_neg_inputs(%i, %i)."%(x+1,gate_type["LowerBoundNeg"])]
        datafile+= ["upper_bound_gate_occurence(%i, %i)."%(x+1,gate_type["UpperBoundOcc"])]
        datafile+= ['']

    datafile+= ['% binding of variables']
    datafile+= ["is_tissue_id(X) :- tissue(X,Y)."]
    datafile+= ["is_mirna(Y) :- data(X,Y,Z)."]
    datafile+= ['is_sign(positive). is_sign(negative).']
    datafile+= ['']
    datafile+= ['']
    
    datafile+= ['%%% Constraints']
    datafile+= ['% number of gates']
    datafile+= ['1 {number_of_gates(X..Y)} 1 :- lower_bound_gates(X), upper_bound_gates(Y).']
    datafile+= ['is_gate_id(1..X) :- number_of_gates(X).']
    datafile+= ['']
    
    datafile+= ['% assignment of gate types']
    datafile+= ['1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).']
    datafile+= ['']

    if EfficiencyConstraint:
        datafile+= ['% inputs for gates (EfficiencyConstraint=True)']
        datafile+= ['feasible_pos_miRNA(MiRNA) :- data(TissueID, MiRNA, high), tissue(TissueID,cancer).']
        datafile+= ['feasible_neg_miRNA(MiRNA) :- data(TissueID, MiRNA, low),  tissue(TissueID,cancer).']
        datafile+= ['feasible_pos_miRNA(MiRNA) :- gate_input(GateID, positive, MiRNA).']
        datafile+= ['feasible_neg_miRNA(MiRNA) :- gate_input(GateID, negative, MiRNA).']
        datafile+= ['']
        datafile+= ['X {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).']
        datafile+= ['X {gate_input(GateID, negative, MiRNA): feasible_neg_miRNA(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).']
        datafile+= ['']
        
    else:
        datafile+= ['% inputs for gates (EfficiencyConstraint=False)']
        datafile+= ['X {gate_input(GateID, positive, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).']
        datafile+= ['X {gate_input(GateID, negative, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).']        
        datafile+= ['']
    
    
    datafile+= ['% at least one input for each gate']
    datafile+= ['1 {gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).']
    datafile+= ['']

    if UniquenessConstraint:
        datafile+= ['% inputs must be unique']
        datafile+= ["{gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_gate_id(GateID)} 1 :- is_mirna(MiRNA)."]
        datafile+= ['']
    
    datafile+= ['% number of inputs is bounded']
    datafile+= ['X {gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} Y :- lower_bound_inputs(X), upper_bound_inputs(Y).']    
    datafile+= ['']
    
    datafile+= ['% occurences of gate types is bounded']
    datafile+= ['{gate_type(GateID,GateType): is_gate_id(GateID)} X :- upper_bound_gate_occurence(GateType,X).']
    datafile+= ['']
    
    datafile+= ['% gates fire condition']
    datafile+= ["gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high)."]
    datafile+= ["gate_fires(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low)."]
    datafile+= ['']
    
    datafile+= ['% prediction of classifier']
    datafile+= ["classifier(TissueID,healthy) :- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID)."]
    datafile+= ["classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID)."]
    datafile+= ['']
    
    datafile+= ['% consistency of classifier and data']
    datafile+= [':- tissue(TissueID,healthy), classifier(TissueID,cancer).']
    datafile+= [':- tissue(TissueID,cancer),  classifier(TissueID,healthy).']
    datafile+= ['']

    if BreakSymmetries:
        datafile+= ['']
        datafile+= ['%%% Breaking symmetries']
        datafile+= ['% gate id symmetries']
        datafile+= ['GateType1 <= GateType2 :- gate_type(GateID1, GateType1), gate_type(GateID2, GateType2), GateID1 <= GateID2.']
        datafile+= ['']
        datafile+= ['']
        
    if OptimizationStrategy==1:
        datafile+= ['% optimization setup 2: first number of inputs then number of gates.']
        datafile+= ['#minimize{ 1@1,(GateID,MiRNA): gate_input(GateID,Sign,MiRNA) }.']
        datafile+= ['#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }.']
        
    elif OptimizationStrategy==2:
        datafile+= ['% optimization setup 1: first number of gates then number of inputs.']
        datafile+= ['#minimize{ 1@1,GateID:gate_input(GateID,Sign,MiRNA) }.']
        datafile+= ['#minimize{ 1@2,(GateID,MiRNA): gate_input(GateID,Sign,MiRNA) }.']
        
    elif OptimizationStrategy==3:
        datafile+= ['% optimization setup 3: only number of inputs.']
        datafile+= ['#minimize{ 1,(GateID,MiRNA):gate_input(GateID,Sign,MiRNA) }.']
        
    elif OptimizationStrategy==4:
        datafile+= ['% optimization setup 4: only number of gates.']
        datafile+= ['#minimize{ 1,GateID:gate_input(GateID,Sign,MiRNA) }.']
                    
    elif OptimizationStrategy==0:
        datafile+= ['% no optimization selected']
    
    datafile+= ['']
    datafile+= ["#show gate_input/3."]

    if FnameASP==None:
        return "\n".join(datafile)
    else:
        with open(FnameASP, 'w') as f:
           f.writelines("\n".join(datafile))

    if not Silent:
        print " created:", FnameASP
        if OptimizationStrategy>0:
            print " now run: gringo %s | clasp --opt-mode=optN --quiet=1"%FnameASP
        else:
            print " now run: gringo %s | clasp -n0"%FnameASP


def gateinputs2pdf(FnamePDF, GateInputs, Silent=False):
    """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """

    GateInputs = GateInputs.strip()
    GateInputs = GateInputs.split()

    
    
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

    if not Silent:
        print "\n--- gateinputs2pdf"
        print " found %i inputs:"%len(GateInputs),GateInputs
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
        false_pos = False
        false_neg = False
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
                false_neg = True
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
            false_pos = True
            malfunction = []
            
        return false_pos, false_neg, malfunction

    return function
                        
    

def check_classifier(FnameCSV, GateInputs):
    """
    Example for GateInputs:

    gate_input(1,positive,g189) gate_input(1,positive,g224) gate_input(2,positive,g89) gate_input(2,positive,g108) gate_input(2,positive,g154) gate_input(3,negative,g31)
    """
    print "\n--- check_classifier"

    miRNAs, rows = csv2rows(FnameCSV)

    print " miRNAs: ", len(miRNAs)
    print " samples:", len(rows)

    false_neg = 0
    false_pos = 0
    
    function = gateinputs2function(GateInputs)
    print " testing each sample against the function.."
    hits = set([])
    for x in rows:
        fp, fn, malfunction = function(x)
        if fp: false_pos += 1
        if fn: false_neg += 1
        
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
 
    return false_neg, false_pos
        
        

def check_csv(FnameCSV):
    """
    counts how many miRNAs are constant across all samples, and
    checks if there are inconsistencies in the data (identical miRNA profile but different annotation)    
    """

    print "\n--- check_csv"

    miRNAs, rows = csv2rows(FnameCSV)
    print " miRNAs: ", len(miRNAs)
    print " samples:", len(rows)
    
    inconsistencies = []
    seen = []
    for x in rows:
        for y in seen:
            if all(x[rna]==y[rna] for rna in miRNAs):
                if x["Annots"]!=y["Annots"]:
                    inconsistencies.append(x["ID"])
        seen.append(x)

    constants = []
    for rna in miRNAs:
        value = rows[0][rna]
        if all(x[rna]==value for x in rows):
            constants.append(rna)
    
    print " inconsistencies (%i): %s"%(len(inconsistencies),",".join(inconsistencies) or "-")
    print " constants (%i): %s"%(len(constants),",".join(constants) or "-")

       
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


def pilot(Parameters, FnamePaths=None):
    """
    This function creates a ASP file, calls gringo and clasp and returns a list of classifiers in "gate_input" format.
    """

    if not FnamePaths:
        FnamePaths = "paths.cfg"
        

    import os
    import subprocess
    import ConfigParser
    

    if not os.path.exists(FnamePaths):
        
        print FnamePaths, "does not exist."
        s=["[Executables]",
           "gringo          = /usr/bin/gringo",
           "clasp           = /usr/bin/clasp"]
        s='\n'.join(s)
        
        with open(FnamePaths,"w") as f:
            f.writelines(s)
            
        print "created",FnamePaths
        print "please check paths and run again."
        return

    
    config = ConfigParser.SafeConfigParser()
    config.read( os.path.join(FnamePaths) )
    CMD_GRINGO = config.get("Executables", "gringo")
    CMD_CLASP  = config.get("Executables", "clasp")

    params_clasp = []
    if Parameters["OptimizationStrategy"]>=1:
        params_clasp = ["--quiet=1", "--opt-mode=optN"]
    else:
        params_clasp = ["-n0"]

    Parameters["FnameASP"] = None
    aspfile = csv2asp(**Parameters)

    cmd_gringo = [CMD_GRINGO]
    cmd_clasp  = [CMD_CLASP] + params_clasp

    try:
        
        proc_gringo = subprocess.Popen(cmd_gringo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc_clasp  = subprocess.Popen(cmd_clasp,  stdin=proc_gringo.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        proc_gringo.stdin.write( aspfile )
        proc_gringo.stdin.close()

        output, error = proc_clasp.communicate()

    except Exception as Ex:
        print Ex
        msg = '\n!!Call to gringo and / or clasp failed.'
        msg+= '\n!!command: "%s"'%' '.join(cmd_gringo+['|']+cmd_clasp)
        msg+= '\n!!Check %s\n'%FnamePaths
        print msg
        raise Ex

    if error:
        print error
        msg = '\n!!Call to gringo and / or clasp failed.'
        msg+= '\n!!command: "%s"'%' '.join(cmd_gringo+['|']+cmd_clasp)
        msg+= '\n!!Check %s\n'%FnamePaths
        print msg
        raise Exception

    hit = False
    answers = []
    for line in output.split('\n'):

        if "gate_input" in line:
            if hit:
                print ">> ANSER OVER SEVERAL LINES! REQURIES BUGFIX"
            else:
                hit = True
                answers+=[line]
        elif "UNSATISFIABLE" in line:
            print "UNSATISFIABLE"
            break
        else:
            hit = False
        
    return answers







    
 
 
 

if __name__=="__main__":
    print "nothing to do"

