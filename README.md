# RnaCancerClassifier

## Files

 * [classifier.py](RnaCancerClassifier/classifier.py) contains the main functions:
   * _csv2asp_ converts a csv data file into a [Potassco](http://potassco.sourceforge.net) ASP file for the construction of a classifier
   * _gateinputs2pdf_ generates a graph-based drawing of a classifier
   * _gateinputs2function_ used internally by _check\_classifier_
   * _check\_classifier_ checks whether a given classifier is consistent with a given data file
 
 * [toy_data.csv](RnaCancerClassifier/toy_data.csv) contains a toy example of input data  
 * [toy_settings.py](RnaCancerClassifier/toy_settings.py) contains an example of input parameters for the [toy_data.csv](RnaCancerClassifier/toy_data.csv)
 

## Example data file
A data file is a 0-1 matrix that contains miRNA expression profiles and whether the tissue is healthy or cancerous.
An example is [toydata.csv](RnaCancerClassifier/toydata.csv):

```
ID, Annots, g1, g2, g3
1,  0,      1,  1,  1
2,  0,      0,  0,  1
3,  1,      0,  1,  0
```
 * `ID` is the row index
 * `Annots` denotes whether the tissue is _healthy_ by `0` or _cancerous_ by `1`
 * `g1, g2, ...` denotes the expression of a miRNA is _low_ by `0` or _high_ by `1`
 

## Example settings file
A settings file calls functions of [classifier.py](RnaCancerClassifier/classifier.py) contains the input parameters 
