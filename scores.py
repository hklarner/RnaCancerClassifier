import csv
import math
import numpy as np
from sklearn.metrics import roc_auc_score

import classifier

#Biochemical parameters:
#(these are the parameters found in the .mat file)
#not sure where they come from
C_1 = 20
C_2 = 10251
FF4_max = 3000
T_max = 9755
Out_max = 50000 #Out_max?!?

def scores(GateInputs, FnameBinaryCSV, FnameOriginalCSV, BinThreshold):

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

	print PositiveGates

	#use Hannes' function to read CSV to dictionary
	data_miRNA, data_samples = classifier.csv2rows(FnameOriginalCSV)
	#use Hannes' check_classifier to count false negative, false positive
	false_neg, false_pos = classifier.check_classifier(FnameBinaryCSV, GateInputs)

	print ""
	print "------------------------------------------------------------------"	
	print "SCORES:"
	print "------------------------------------------------------------------"	
	print ""
	print "Biochemical parameters used:"	
	print "-----------"
	print "C_1: "+ str(C_1)
	print "C_2: "+ str(C_2)
	print "FF4_max: "+ str(FF4_max)
	print "T_max: "+ str(T_max)
	print "Out_max: "+ str(Out_max)
	print ""
	print "Circuit outputs:"	
	print "-----------"
	#for margins
	first_term_up = float(0)
	second_term_up = float(0)
	first_term_down = float(0) #number of positive observations
	second_term_down = float(0) #number of negative observations

	min_first_term = float(1000000000) #TODO large number
	max_second_term = float(0)
	
	NumberPosSamples = 0
	NumberNegSamples = 0

	#circuit output for each sample
	annots = []
	circuit_outputs = []
	for x in data_samples:
		annots.append(int(x["Annots"]))
		if int(x["Annots"]) == 1:
			NumberPosSamples = NumberPosSamples +1
		if int(x["Annots"]) == 0:
			NumberNegSamples = NumberNegSamples +1
		#calculate FF4
		if not PositiveGates:
			FF4_value = 0
		else:
			FF4_value = FF4(x,PositiveGates)	
		
		#calculate circuit output
		circ_out = circuit_output(x,NegativeGates,FF4_value)
		circuit_outputs.append(circ_out)
	
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
	print ""
	print "Margins:"	
	print "-----------"
	average_margin = (first_term_up / first_term_down) - (second_term_up / second_term_down)
	print "Average margin of Circuit (C_MarginA): "+str(average_margin)	
	
	worst_margin = min_first_term - max_second_term
	print "Worst margin of Circuit (C_MarginW): "+str(worst_margin)	
	#PERFORMANCE SCORE 2: Margins
	MyLambda = 0.5
	score2 = (MyLambda*average_margin) + ((1-MyLambda)*worst_margin)
	print ""
	print "Classification:"
	print "-----------"
	print "Number of positive samples (cancer) : "+str(NumberPosSamples)
	print "Number of negative samples (healthy) : "+str(NumberNegSamples)

	print "Number of false positive : "+str(false_pos)
	print "Number of false negative : "+str(false_neg)
	true_pos = NumberPosSamples - false_neg
	true_neg = NumberNegSamples - false_pos
	print "Number of true positive : "+str(true_pos)
	print "Number of true negative : "+str(true_neg)
	sensitivity = float(true_pos) / float(NumberPosSamples)
	specificity = float(true_neg) / float(NumberNegSamples)	
	false_neg_rate = float(false_neg) / float(NumberPosSamples)
	false_pos_rate = float(false_pos) / float(NumberNegSamples)
	print ""
	print "Statistics:"
	print "-----------"
	print "Sensitivity : "+str(sensitivity)
	print "Specificity : "+str(specificity)
	print "False positive rate : "+str(false_pos_rate)
	print "False negative rate : "+str(false_neg_rate)
	print ""
	print "Binarization margins:"
	print "-----------"
	BinMarginsCSV = binaryvalue_margins(FnameOriginalCSV, BinThreshold)
	print "Wrote .csv file with margins for binary values:"
	print str(FnameOriginalCSV[:-4])+"_binarymargins.csv"
	print ""
	print "Performance:"
	print "-----------"
	y_true = np.array(annots)
	y_scores = np.array(circuit_outputs)
	auc = roc_auc_score(y_true, y_scores)
	print "First performance score: Area under the ROC curve: " + str(auc)
	print "Second performance score: Margins (lambda=0.5): "+ str(score2)
	print "                          Margins (lambda=1.0): "+ str(average_margin)
	print ""

def binaryvalue_margins(FnameOriginalCSV, BinThreshold):
	original_miRNA, original_samples = classifier.csv2rows(FnameOriginalCSV)

	with open(FnameOriginalCSV[:-4]+"_binarymargins.csv","wb") as csvfile:
    		mywriter = csv.writer(csvfile, delimiter=',')

		header = ["ID" , "Annots"]
		for rna in original_miRNA:
			header.append(str(rna))
		mywriter.writerow(header)

		for x in range(0,len(original_samples)):
			marginrow = [str(x+1)]
			marginrow.append(original_samples[x]["Annots"])
			for rna in original_miRNA:			
				orgval = float(original_samples[x][rna].replace(',','.'))
				#calculate binary margin for each value
				bin_marg = round(abs(float(math.log10(orgval))-float(math.log10(BinThreshold))),4)
				marginrow.append(str(bin_marg))
			mywriter.writerow(marginrow)
		BinMarginsCSV = FnameOriginalCSV[:-4]+"_binarymargins.csv"

	return BinMarginsCSV

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

	first =  int(PositiveGatesInput[0][0])
	last =  int(PositiveGatesInput[-1][0])

	for i in range(first,last+1):
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

#our circuit
#GateInputs = "gate_input(1,negative,g3) gate_input(2,negative,g4)"

#given circuit
GateInputs = "gate_input(1,negative,g7) gate_input(2,negative,g6) gate_input(3,negative,g4) gate_input(4,negative,g3) "
GateInputs+= "gate_input(5,positive,g1) gate_input(5,positive,g2) gate_input(5,positive,g8) "
GateInputs+= "gate_input(6,positive,g1) gate_input(6,positive,g5) gate_input(6,positive,g8)"

FnameBinaryCSV = "/home/mi/katinkab/synthbio/RnaCancerClassifier/casestudies/C2.csv"
FnameOriginalCSV = "/home/mi/katinkab/synthbio/RnaCancerClassifier/casestudies/C2_original.csv"
BinThreshold = 250
scores(GateInputs, FnameBinaryCSV, FnameOriginalCSV, BinThreshold)
