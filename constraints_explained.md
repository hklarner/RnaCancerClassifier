
#### The constraints explained
This file explains all constraints in detail.

### `tissue(1,cancer). tissue(2,healthy).`
Each tissue sample, that is, each row in the data file, is either _healthy_ or _cancerous_ as determined by the column with header _Annots_.
The first argument is the integer _TissueID_, the second one of the constants `healthy` or `cancer`.

### `is_tissue_id(X) :- tissue(X,Y).`
The predicate `is_tissue_id(X)` is not a constraint. It is used for binding values of _TissueID_ in other constraints.

### `data(1,g1,high). data(1,g2,low).`
These facts determine the expression levels of miRNAs in tissue samples.
The first argument is the integer _TissueID_, the second a constant _MiRNA_ value, the third one of the constants `high` or `low`.

### `is_mirna(Y) :- data(X,Y,Z).`
The predicate `is_mirna(Y)` is not a constraint. It is used for binding values of _MiRNA_ in other constraints.

### `is_gate_type(1).`
Binds constraints related to gate types.
The argument is the integer _GateID_.

### `upper_bound_pos_inputs(2, 2). lower_bound_pos_inputs(2, 2).`
These facts specify the upper and lower bounds on the number of positive and negative inputs for each gate type.
It takes two arguments, the _GateType_ and the value of the bound.

### `upper_bound_gate_occurence(1, 2).`
This fact specifies the upper bound on the number of occurences of a gate type in the classifier.
The first argument is the _GateID_ the second is the value of the bound.

### `is_sign(positive). is_sign(negative).`
These facts are used to bind value of _Sign_.

### `upper_bound_inputs(10).`
This fact specifies the upper bound on the total number of inputs for the classifier.

### `1 {number_of_gates(1..6)} 1. is_integer(1..6).`
This constraint determines the number of gates that are used in the classifier.
The predicate `number_of_gates` is true for exactly one integer value between 1 and the upper bound given by the user.
The predicate `is_integer` is used to generate all _GateID_s between 1 and the chosen number of gates.

### `is_gate_id(GateID) :- number_of_gates(X), is_integer(GateID), GateID<=X.`
This constraint generates a _GateID_ for each number between 1 and `number_of_gates(X)`.
The predicate `is_gate_id` is used for binding values of _GateID_.

### `1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).`
This constraint assigns a _GateType_ to every _GateID_.
The predicates `is_gate_type(X)` and `is_gate_id(GateID)` are just binding admissible values of _GateType_ and _GateID_.

### `feasible_pos_miRNA(MiRNA) :- data(TissueID, MiRNA, high), tissue(TissueID,cancer).`
These constraints define feasible positive and negative inputs.
They are based on the observation that inputs to the classifier must be variables that are not constant in the data.
More specifically, a positive input must be `high`ly expressed on some `cancer` sample and a negative input `low`ly.

### `X {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).`
This constraint enforces that each _GateID_ has the correct number of positive and negative inputs, bounded by the _GateType_ parameters.

### `1 {gate_input(GateID, Sign, MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).`
This is a safety constraint in case the lower bounds for inputs for a gate type are 0.
It forbids a gate to have no inputs at all.

### `{gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_gate_id(GateID)} 1 :- is_mirna(MiRNA).`
This constraint enforces that a _MiRNA_ can only appear once in a classifier.

### `{gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} X :- upper_bound_inputs(X).`
This constraint enforces that the number of gate inputs is smaller that or equal to `upper_bound_inputs(X)`.

### `{gate_type(GateID,GateType): is_gate_id(GateID)} X :- upper_bound_gate_occurence(GateType,X).`
This constraint enforces that the number of gates of each _GateType_ is bounded from above by the user given occurence value.

### `GateType1 <= GateType2 :- gate_type(GateID1, GateType1), gate_type(GateID2, GateType2), GateID1 <= GateID2.`
This is the first symmetry breaking constraint.
It says that gate ids should be assinged to the smallest possible gate types.

### `MiRNA1<=MiRNA2 :- gate_type(GateID1, GateType), gate_type(GateID2, GateType), gate_input(GateID1,Sign,MiRNA1), gate_input(GateID2,Sign,MiRNA2), GateID1<=GateID2.`
This is the second symmetry breaking constraint.
If two gates are of the same _GateID_ then the inputs of the one with the smaller _GateID_ should be smaller than the inputs of the one with the larger _GateID_.

**not sure if this constraint is correct**

### `gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high).`
A gate fires for a _TissueID_ if one of its _positive_ inputs is _high_ly expressed or one of its _negative_ inputs is _low_ly expressed.

### `classifier(TissueID,healthy) :- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID).`
The classifier predicts a _healthy_ _TissueID_ if there is a _GateID_ that does not fire for that tissue.

### `classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID).`
The classifier predict _cancer_ for a _TissueID_ if it does not predict a _healthy_ _TissueID_.
Note that the encoding via negation is neccessary since the classifier is a conjunction of gates.


### `:- tissue(TissueID,healthy), classifier(TissueID,cancer).`
The classifier must agree with the tissue samples.




























