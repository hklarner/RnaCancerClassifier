# RnaCancerClassifier
This project is about converting miRNA expression profiles of healthy and cancerous tissue samples into an Answer Set Program (ASP)
that constructs an optimal Boolean classifier for distinguishing between these tissue types in terms of their miRNA fingerprint.

Mathematically, a classifier is a Boolean expression where a variable represents _high_ or _low_ presence of a particular miRNA.
The structure of the Boolean expression should be constrained by the types of biochemical circuits that may be synthesized in a laboratory.


## What is a classifier?
A classifier is a Boolean expression that must be given in _conjunctive normal form_ (CNF).
In this context, each (disjunctive) term of a CNF is called _gate_.
If the expression evaluates to `1`, i.e.,  iff all gates evaluate to `1`, then the classifier predicts cancerous tissue.
An example of a classifier with three gates and six inputs is:

```
 (g7 + g12 + !g13) * (g2 + g5) * (!g8)
```
where `g7` represents the expression of miRNA number seven, `+` means disjunction, `*` means conjunction and `!` means negation.


#### types of constraints
Currently we have implemented the following constraints:

 * upper bound for number of total inputs
 * upper bound of number of gates
 * specification of admissible _gate types_ in terms of upper bounds of the numbers of negated and non-negated inputs
 
In practice it is desirable to compute classifiers with a minimal number of gates or inputs or both.
We have implemented the following optimization strategies:

 * first minimize number of gates, then minimize total number of inputs
 * first minimize total number of inputs, then minimize number of gates
 * only minimize total number of inputs
 * only minimize number of gates

 

## Example
#### input data
A data file is a 0-1 matrix that contains miRNA expression profiles and whether the tissue is healthy or cancerous.
An example is [toy_data.csv](./toy_data.csv):

```
ID, Annots, g1, g2, g3
1,  0,      1,  1,  0
2,  0,      0,  0,  1
3,  1,      0,  1,  0
```
 * `ID` is the row index
 * `Annots` specifies whether a tissue is _healthy_ with `0` or _cancerous_ with `1`
 * `g1, g2, ...` specifies whether the expression of a miRNA in a tissue is _low_ with `0` or _high_ with `1`
 

#### generation of the ASP file
An ASP file is created by a call of the function `classifier.csv2asp`.
Its parameters specify all the classifier constraints.
An example is given in the file [toy_settings.py](./toy_settings.py).
The parameters are specified at the top of the file.

```
FnameCSV = "toy_data.csv"
FnameASP = "toy_classifier.asp"
UpperBoundInputs = 3
UpperBoundGates  = 2
GateTypes = [(1,1),]
EfficiencyConstraint = True
OptimizationStrategy = 1
```

The meaning of the parameters is explained below:

 * _FnameCSV_ the data file
 * _FnameASP_ the ASP file to be generated
 * _UpperBoundInputs_ upper bound on total number of inputs
 * _UpperBoundGates_ upper bound on number of gates
 * _GateTypes_ a list of tuples `(x,y)` where `x` is the upper bound of non-negated inputs and `y` the upper bound of negated inputs of a gate of that type
 * _EfficiencyConstraint_ should be kept at `True`
 * _OptimizationStrategy_ a number between one and four where
   * 1 = minimize number of gates, then minimize number of inputs
   * 2 = minimize number of inputs, then minimize number of gates
   * 3 = minimize number of inputs
   * 4 = minimize number of gates


To generate the ASP file with the given constraints, call the function `classifier.csv2asp`:

```
import classifier

if __name__=="__main__":
    if 1 :
        classifier.csv2asp(
            FnameCSV,
            FnameASP,
            UpperBoundInputs,
            UpperBoundGates,
            GateTypes,
            EfficiencyConstraint,
            OptimizationStrategy)
```

Now use the ASP solver [Potassco](http://potassco.sourceforge.net) to compute the optimal classifiers:

```
$ gringo toy_classifier.asp | clasp --opt-mode=optN
Solving...
Answer: 1
gate_input(1,positive,g2) gate_input(2,negative,g1)
Optimization: 2 2
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

which tells us that there are four optimal models:

```
gate_input(1,negative,g3) gate_input(2,negative,g1)
gate_input(1,positive,g2) gate_input(2,negative,g1)
gate_input(2,negative,g3) gate_input(1,negative,g1)
gate_input(2,positive,g2) gate_input(1,negative,g1)
```

The classifier is defined in terms of the inputs to each gate.
The predicate _gate\_input_ takes three arguments: the ID of the gate, whether the input is positive or negated and the name of the miRNA.
As Boolean expressions the classifiers are

```
!g3 * !g1
 g2 * !g1
!g1 * !g3
!g1 *  g2
```

#### generation of a PDF drawing of a classifier
To create a drawing of a classifier call the function `classifier.gateinputs2pdf`:

```
   GateInputs = "gate_input(2,positive,g2) gate_input(1,negative,g1)"
   FnamePDF = "toy_classifier.pdf"
   classifier.gateinputs2pdf(FnamePDF, GateInputs)
```
The function require the program [dot](www.graphviz.org).
The output is the file [toy_classifier.pdf](./toy_classifier.pdf) which is shown below:
![toy_classifier.pdf](./toy_classifier.pdf)


## Files

 * [classifier.py](./classifier.py) contains the main functions:
   * **csv2asp** converts a csv data file into a [Potassco](http://potassco.sourceforge.net) ASP file for the construction of a classifier
   * **gateinputs2pdf** generates a graph-based drawing of a classifier
   * **gateinputs2function** used internally by _check\_classifier_
   * **check\_classifier** checks whether a given classifier is consistent with a given data file
 
 * [toy_data.csv](./toy_data.csv) an example of input data  
 * [toy_settings.py](./toy_settings.py) an example of parameters settings
