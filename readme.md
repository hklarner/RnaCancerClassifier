# RnaCancerClassifier
This project is about converting miRNA expression profiles of healthy and cancerous tissue samples into an Answer Set Program (ASP)
that constructs an optimal Boolean classifier for distinguishing between these tissue types in terms of their miRNA fingerprint.

- The code is written in Python 2
- The computation of the classifiers requires clasp and gringo from [Potassco](http://potassco.sourceforge.net)
- Send questions / remarks to hannes.klarner@fu-berlin.de or leave an [issue](https://github.com/hklarner/RnaCancerClassifier/issues)

## What is a classifier?
Mathematically, a classifier is a Boolean expression where a variable represents _high_ or _low_ presence of a particular miRNA.
The structure of the Boolean expression should be constrained by the types of biochemical circuits that may be synthesized in a laboratory.

First, it must be given in _conjunctive normal form_ (CNF).
In this context, each (disjunctive) term of a CNF is called _gate_.
If the expression evaluates to `1`, i.e.,  iff all gates evaluate to `1`, then the classifier predicts cancerous tissue.
An example of a classifier with three gates and six inputs is:

```
 (g7 + g12 + !g13) * (g2 + g5) * (!g8)
```
where `g7` represents the expression of miRNA number seven, `+` means disjunction, `*` means conjunction and `!` means negation.


#### types of constraints
Currently we have implemented the following constraints:

 * upper bound for _number of total inputs_
 * upper bound of _number of gates_
 * specification of admissible _gate types_ in terms of
   * bounds on the numbers of negated and non-negated inputs and
   * bound on occurences of a gate type in the classifier
 
In practice it is desirable to compute classifiers with a minimal number of gates or inputs or both.
We have implemented the following optimization strategies:

 * first minimize number of gates, then minimize total number of inputs
 * first minimize total number of inputs, then minimize number of gates
 * only minimize total number of inputs
 * only minimize number of gates

 

## Example
#### input data
A data file is a 0-1 matrix that contains miRNA expression profiles and whether the tissue is healthy or cancerous.
An example is [toy.csv](./toy.csv):

```
ID, Annots, g1, g2, g3
1,  0,      1,  1,  0
2,  0,      0,  0,  1
3,  1,      0,  1,  0
```
 * `ID` is the row index
 * `Annots` specifies whether a tissue is _healthy_ with `0` or _cancerous_ with `1`
 * `g1, g2, ...` specifies whether the expression of a miRNA in a tissue is _low_ with `0` or _high_ with `1`
 

#### generate the ASP file
An ASP file is created by a call of the function `classifier.csv2asp`.
Its parameters specify all the classifier constraints.
An example is given in the file [toy.py](./toy.py).
The parameters are specified at the top of the file.

```
FnameCSV = "toy.csv"
FnameASP = "toy.asp"
UpperBoundInputs = 3
UpperBoundGates  = 2
GateTypes = [{"LowerBoundPos":0,"UpperBoundPos":1,
              "LowerBoundNeg":0,"UpperBoundNeg":0,
              "UpperBoundOcc":1},
             {"LowerBoundPos":0,"UpperBoundPos":0,
              "LowerBoundNeg":0,"UpperBoundNeg":1,
              "UpperBoundOcc":2}]
EfficiencyConstraint = True
OptimizationStrategy = 1
```

The meaning of the parameters is explained below:

 * _FnameCSV_ the data file
 * _FnameASP_ the ASP file to be generated
 * _UpperBoundInputs_ upper bound on total number of inputs
 * _UpperBoundGates_ upper bound on number of gates
 * _GateTypes_ a dictionary with keys
   * `LowerBoundPos` = lower bound of positive inputs to gate
   * `UpperBoundPos` = upper bound of positive inputs to gate
   * `LowerBoundNeg` = lower bound of negative inputs to gate
   * `UpperBoundNeg` = upper bound of negative inputs to gate
   * `UpperBoundOcc` = upper bound of occurences of gate in classifier
   
    of tuples `(x,y)` where `x` is the upper bound of non-negated inputs and `y` the upper bound of negated inputs of a gate of that type
 * _EfficiencyConstraint_ should be kept at `True`
 * _OptimizationStrategy_ a number between one and four where
   * 1 = minimize number of gates, then minimize number of inputs
   * 2 = minimize number of inputs, then minimize number of gates
   * 3 = minimize number of inputs
   * 4 = minimize number of gates


To generate the ASP file with the given constraints, call the function `classifier.csv2asp`:

```
    classifier.csv2asp(FnameCSV, FnameASP, UpperBoundInputs, UpperBoundGates,
                       GateTypes, EfficiencyConstraint, OptimizationStrategy)
```

The output is
```
--- csv2asp
 input file: toy.csv
 upper bound on inputs: 3
 upper bound on gates: 1
 gate types (upper bound positive / negative inputs): [(3, 3)]
 efficiency constraints: True
 optimization strategy: 2 (minimize inputs then minimize gates)
 miRNAs:  3
 samples: 3
 created: toy.asp
 now run: gringo toy.asp | clasp --opt-mode=optN
```

Now use the ASP solver [Potassco](http://potassco.sourceforge.net) to compute the optimal classifiers:

```
$ gringo toy.asp | clasp --opt-mode=optN --quiet=1
Solving...
Answer: 1
gate_input(1,negative,g3) gate_input(2,negative,g1)
Optimization: 2 2
Answer: 2
gate_input(1,positive,g2) gate_input(2,negative,g1)
Optimization: 2 2
Answer: 3
gate_input(2,negative,g3) gate_input(1,negative,g1)
Optimization: 2 2
Answer: 4
gate_input(2,positive,g2) gate_input(1,negative,g1)
Optimization: 2 2
OPTIMUM FOUND

Models       : 5     
  Optimum    : yes
  Optimal    : 4
```

which tells us that there are four optimal classifiers:

```
gate_input(1,negative,g3) gate_input(2,negative,g1)
gate_input(1,positive,g2) gate_input(2,negative,g1)
gate_input(2,negative,g3) gate_input(1,negative,g1)
gate_input(2,positive,g2) gate_input(1,negative,g1)
```

A classifier is defined in terms of the inputs to each of its gates.
The three arguments of each _gate\_input_ are: the ID of the gate, whether the input is positive or negated and the name of the miRNA.
Converted into Boolean expressions the classifiers above are

```
!g3 * !g1
 g2 * !g1
!g1 * !g3
!g1 *  g2
```

#### visualize a classifier
To create a drawing of a classifier call the function `classifier.gateinputs2pdf`:

```
   GateInputs = "gate_input(2,positive,g2) gate_input(1,negative,g1)"
   FnamePDF = "toy.pdf"
   classifier.gateinputs2pdf(FnamePDF, GateInputs)
```
The function requires the program [dot](www.graphviz.org).
The result is the file [toy.pdf](./toy.pdf):

```
--- gateinputs2pdf
 found 2 inputs: ['gate_input(2,positive,g2)', 'gate_input(1,negative,g1)']
 created toy.pdf
```


#### check consistency
All classifiers obtained from the ASP solver are by definition consistent with the data.
Sometimes it may be necessary to check whether a classifier that is not obtained from the ASP solver is consistent with a given data file.
In that case you have to convert the classifier into a _gate\_input_ string (by hand) and call the function `classifier.check_classifier`:

```
    GateInputs = "gate_input(1,negative,g1)"
    classifier.check_classifier(FnameCSV, GateInputs)
```
The output informs you of all encountered inconsistencies (malfunctions):

```
--- check_classifier
 miRNAs:  3
 samples: 3
 found 1 input(s) for function generation: ['gate_input(1,negative,g1)']
 testing each sample against the function..
 ** found malfunction:
    gate_id = 1
    gate_inputs = set([('g1', 'negative')])
    miRNA_expressions = g1=0
    tissue = healthy
    tissue_id = 2
 classifier = gate_input(1,negative,g1)
 data = toy.csv
 result = 1 inconsistencies set(['2'])
```

#### check csv data
To check whether there are _inconsistencies_ or _constants_ in the data call the function `classifier.check_csv`.
It lists all miRNAs that are constant across all samples, i.e., always _high_ or always _low_,
and checks if there are profiles that are identical in terms of the miRNA profile but differ w.r.t. to the annotation.
If there are inconsistencies then there is no classifier.


## Files

 * [classifier.py](./classifier.py) contains the main functions:
   * **csv2asp** converts a csv data file into a [Potassco](http://potassco.sourceforge.net) ASP file for the construction of a classifier
   * **gateinputs2pdf** generates a graph-based drawing of a classifier
   * **gateinputs2function** used internally by _check\_classifier_
   * **check\_classifier** checks whether a given classifier is consistent with a given data file
   * **mat2csv** converts a mat file into a csv file in the required format
 
 * [toy.csv](./toy.csv) an example of input data  
 * [toy.py](./toy.py) an example of parameters settings
