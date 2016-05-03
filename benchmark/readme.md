

### Benchmarks

#### Random Matrix Experiments (benchmark1)
The script `benchmark1_step1.r` generates random binary matrices and stores them in files called ´csvs/matrix_<healthy>_<rows>x<columns>.csv`.
It generates matrices with 10 to 100 rows and columns and tissues with a probability of being healthy that increase from 0.05 to 0.95 in steps of 0.05.

The script `benchmark1_step2.py` first generates a `asp` file for each random matrix of step 1.
It then calls gringo for each random data set with the _Beerenwinkel_ settings and records 

_Beerenwinkel settings_:

 * UpperBoundInputs = 10
 * UpperBoundGates  = 6
 * GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":3,
              "LowerBoundNeg":0,"UpperBoundNeg":0,
              "UpperBoundOcc":2},
             {"LowerBoundPos":0,"UpperBoundPos":0,
              "LowerBoundNeg":0,"UpperBoundNeg":1,
              "UpperBoundOcc":4}]
 * EfficiencyConstraint = True
 * OptimizationStrategy = 2

#### Random Classifier Experiments (benchmark2)

