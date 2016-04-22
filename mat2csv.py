# Parser to read matlab files (Sim_Sample.mat) 
# 	and write csv files (Sim_Sample_binary.csv)
# 	usable as input for classifier.py

import numpy as np
from scipy.io import loadmat
import csv

#Choose datafile
filename = raw_input("Please enter file name: ")

# Threshold (0 if variable<threshold else 1)
threshold = raw_input("Please choose binarization threshold (0 if variable<threshold else 1): ")
print "Threshold used for binarization: "+str(threshold)

# Read .mat file
datafile = loadmat(filename)

col = datafile['SimDataHeike']['Values'][0,0][0,:]
row = datafile['SimDataHeike']['Values'][0,0][:,0]
print "Number of samples: "+str(col.size)
print "Number of miRNAs: "+str(row.size)

# ID column
id_column = []
id_column.append("ID")
for i in range(0,col.size):
	id = i
	id_column.append(i+1)

# Write .csv file
np.savetxt(str(filename[:-4])+'_binary.csv', 
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
print "Number of cancer cells: "+str(cancer_count)
	
oldfile = open(str(filename[:-4])+'_binary.csv')
olddata = [item for item in csv.reader(oldfile)]
oldfile.close()    

newdata = []
 
for i, item in enumerate(olddata):
    	try:
       		item.append(annots_column[i])
    	except IndexError, e:
        		item.append("placeholder")
    	newdata.append(item)
 
newfile = open(str(filename[:-4])+'_binary.csv', 'w')
csv.writer(newfile).writerows(newdata)
newfile.close()
	
# Values of miRNAs in columns            
# First row to end
for r in range(0,row.size):      
           
	oldfile = open(str(filename[:-4])+'_binary.csv')
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
 
	newfile = open(str(filename[:-4])+'_binary.csv', 'w')
	csv.writer(newfile).writerows(newdata)
	newfile.close()
	
# Get classifier
for c in range(0,6):
	input = datafile['SimDataHeike']['Synthesis_Function'][0,0][0,c]
	for r in range(0,3):
		if input[r] > 0:
			print "gate_input("+str(c+1)+",positive,"+str(input[r])+")"
		if input[r] < 0:
			nosign = input[r]*-1
			print "gate_input("+str(c+1)+",negative,"+str(nosign)+")"
