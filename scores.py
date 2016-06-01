import csv
import math

#Biochemical parameters:
#(these are the parameters found in the .mat file)
#not sure where they come from
C_1 = 20
C_2 = 10251
FF4_max = 3000
T_max = 9755
Out_max = 50000 #Out_max?!?

def scores(GateInputs, FnameBinaryCSV, FnameOriginalCSV):

	print "Biochemical parameters:"
	print "C_1: "+ str(C_1)
	print "C_2: "+ str(C_2)
	print "FF4_max: "+ str(FF4_max)
	print "T_max: "+ str(T_max)
	print "Out_max: "+ str(Out_max)

	#INPUT: Classifier Gates
	NegativeGates = []
	Inputs = GateInputs.split()
	for x in Inputs:
		if "negative" in x:
			interstep = x.split(",negative,")
			miRNA = interstep[1][:-1] 
			gatenumber = interstep[0][11:] 
			NegativeGates.append(gatenumber+", "+miRNA)

	PositiveGates = []
	for x in Inputs:
		if "positive" in x:	
			interstep = x.split(",positive,")
			miRNA = interstep[1][:-1]
			gatenumber = interstep[0][11:] 
			PositiveGates.append(gatenumber+", "+miRNA)

	#use Hannes' function to read CSV to dictionary
	data_miRNA, data_samples = csv2rows(FnameOriginalCSV)

	#for margins
	first_term_up = float(0)
	second_term_up = float(0)
	first_term_down = float(0) #number of positive observations
	second_term_down = float(0) #number of negative observations
	min_first_term = float(10000000) #TODO large number
	max_second_term = float(0)

	#circuit output for each sample
	for x in data_samples:
		#calculate FF4
		FF4_value = FF4(x,PositiveGates)	
		
		#calculate circuit output
		circ_out = circuit_output(x,NegativeGates,FF4_value)
	
	#average classification margin for whole circuit
		add_first = float(x["Annots"])*float(math.log10(circ_out))
		first_term_up = first_term_up + add_first
		if add_first != 0:
			if add_first < min_first_term:
				min_first_term = add_first
		first_term_down = first_term_down + float(x["Annots"])
		
		add_sec = float(1-float(x["Annots"]))*float(math.log10(circ_out))
		second_term_up = second_term_up + add_sec
		if add_sec > max_second_term:
			max_second_term = add_sec
		second_term_down = second_term_down + float(1-float(x["Annots"]))	

	average_margin = (first_term_up / first_term_down) - (second_term_up / second_term_down)
	print "Average margin of Circuit (C_MarginA): "+str(average_margin)	
	
	worst_margin = min_first_term - max_second_term
	print "Worst margin of Circuit (C_MarginW): "+str(worst_margin)	

	#PERFORMANCE SCORE 2: Margins
	MyLambda = 0.5
	score2 = (MyLambda*average_margin) + ((1-MyLambda)*worst_margin)
	print "The second performance score of the cicuit is: "+ str(score2)

def circuit_output(Sample,NegativeGatesInput,FF4_Val):
	neg_vector = []	
	for allinputs in NegativeGatesInput:
		gateinput = allinputs.split(", ")
		neg_vector.append(Sample[str(gateinput[1])])
	neg_vector.append(str(str(FF4_Val).replace('.',',')))
	f1_forout = f_1(neg_vector)
	circ_out = float(Out_max) * f1_forout
	print "Circuit Output (mols/cell) for sample "+Sample["ID"]+": "+str(circ_out)
	return circ_out


def FF4(Sample,PositiveGatesInput):
	ff4_sum = float(0)
	for i in [5,6]: #TODO
		vector = []	
		for allinputs in PositiveGatesInput:
			gateinput = allinputs.split(", ")
			if int(gateinput[0])==i:
				vector.append(Sample[str(gateinput[1])])
		
		entry = f_1(vector)	
		ff4_sum = ff4_sum + entry
	ff4_f2_result = f_2(ff4_sum)
	FF4 =float(FF4_max)*ff4_f2_result
	return FF4

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

def f_1(InputVector):
	sum_num = float(0)
	for x in InputVector:
		sum_num = sum_num+float(x.replace(',','.'))

	sum_denom = C_1 + sum_num
	out = 1 - (sum_num / sum_denom)
	return out
	
def f_2(InputFloat):
	out = float(InputFloat) / ((float(C_2) / float(T_max)) + float(InputFloat))
	return out

GateInputs = "gate_input(1,negative,g7) gate_input(2,negative,g6) gate_input(3,negative,g4) gate_input(4,negative,g3) "
GateInputs+= "gate_input(5,positive,g1) gate_input(5,positive,g2) gate_input(5,positive,g8) "
GateInputs+= "gate_input(6,positive,g1) gate_input(6,positive,g5) gate_input(6,positive,g8)"

FnameBinaryCSV = "/home/mi/katinkab/synthbio/RnaCancerClassifier/casestudies/C2.csv"
FnameOriginalCSV = "/home/mi/katinkab/synthbio/RnaCancerClassifier/casestudies/C2_original.csv"
scores(GateInputs, FnameBinaryCSV, FnameOriginalCSV)
