

   
   
#### Benchmark1: Random Matrix Experiments
The script `benchmark1.sh` loops over `rows` and `cols`, each increasing from 10 to 100, and `healthy`, which increases from 0.05 to 0.95 in steps of 0.05.
For each combination of values it creates a random binary matrix and tissue annotation vector which is stored in `benchmark1_tmp.csv`.
The script converts the data file into the asp file `benchmark1_tmp.asp` using the python script `benchmark1.py` and passes the result to gringo and clasp.
If the asp problem is satisfiable it records all parameters and information about the CPU time to obtain the solutions and how many there are.
The results are stored in `benchmark1_results.csv`.

Notes:

   * unsatisfiable asp files are ignored

#### Benchmark2: Random Classifier Experiments


#### Benchmark3: Heike's Slices


