


import os
import subprocess
import ConfigParser


def run():

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



if __name__=="__main__":
    run()
