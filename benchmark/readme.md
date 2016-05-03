

### Benchmarks

#### Random Matrix Experiments (benchmark1)
The script `benchmark1_step1.r` generates random binary matrices and stores them in files called ´csvs/matrix_<healthy>_<rows>x<columns>.csv`.
It generates matrices with 10 to 100 rows and columns and tissues with a probability of being healthy that increase from 0.05 to 0.95 in steps of 0.05.

The script `benchmark1_step2.py` first generates an `asp` file for each random matrix of step 1 using the _Beerenwinkel settings_ (see file).
It then calls gringo for each random data set and records various times and numbers in the file `benchmark1_results.csv`.


#### Random Classifier Experiments (benchmark2)


