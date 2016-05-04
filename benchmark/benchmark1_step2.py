

import sys
sys.path = ["../"] + sys.path
import classifier
import os
import subprocess
import ConfigParser



def run():
    print 'this script converts "./csvs/matrix_<rows>_<columns>_<healthy>.csv" files into asp'
    counter = 0
    for FnameCSV in os.listdir("./csvs/"):
        if FnameCSV[:6]!="matrix": continue
        if FnameCSV[-4:]!=".csv": continue
        counter+=1

        x = FnameCSV.split('.')[0]
        rows,cols,prob = map(int,x.split('_')[1:])
        prob = 0.01 * prob

        FnameASP = FnameCSV.replace('.csv','.asp')

        classifier.csv2asp( './csvs/'+FnameCSV,
                            './csvs/'+FnameASP,
                            UpperBoundInputs = 10,
                            UpperBoundGates  = 6,
                            GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":3,
                                          "LowerBoundNeg":0,"UpperBoundNeg":0,
                                          "UpperBoundOcc":2},
                                         {"LowerBoundPos":0,"UpperBoundPos":0,
                                          "LowerBoundNeg":0,"UpperBoundNeg":1,
                                          "UpperBoundOcc":4}],
                            EfficiencyConstraint = True,
                            OptimizationStrategy = 2,
                            Silent=True)

    
    print " converted %i files"%counter



if __name__=="__main__":
    run()



def gringo():
    # brauche ich zur Zeit doch nicht.

    if not os.path.isfile("paths.cfg"):
        print 'could not find "paths.cfg" for paths to gringo and clasp'
        f = open("paths.cfg", "w")
        f.write("\n".join(["[Paths]",
                           "gringo = /gringo-4.4.0/gringo",
                           "clasp  = /clasp-3.1.1/clasp-3.1.1-x86-linux"]))
        f.close()
        print 'created "paths.cfg", add paths to gringo and clasp'
        return
        

    with open("paths.cfg", "r") as f:
        config = ConfigParser.SafeConfigParser()
        config.read("paths.cfg")
        CMD_GRINGO = config.get("Paths", "gringo")
        CMD_CLASP  = config.get("Paths", "clasp")


    cmd_gringo = [CMD_GRINGO, FnameASP]
    proc_gringo = subprocess.Popen(cmd_gringo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    cmd_clasp  = [CMD_CLASP, "--opt-mode=optN", "--quiet=1"]
    proc_clasp  = subprocess.Popen(cmd_clasp, stdin=proc_gringo.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = proc_clasp.communicate()
