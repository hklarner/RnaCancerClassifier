
% ASP constraints for computing a classifier (in this case a Boolean Function),
% that agrees with given tissue data (either cancerous or healthy) and
% and satisfies certain structural constraints.
% Note: a classifier is the conjunction of disjunctive gates (CNF)
% written by K. Becker and H. Klarner, March 2016, FU Berlin.

% InputFile = toy.csv
%  upper bound on inputs: 10
%  upper bound on gates: 2
%  gate types: [{'UpperBoundOcc': 1, 'LowerBoundNeg': 0, 'UpperBoundNeg': 0, 'LowerBoundPos': 0, 'UpperBoundPos': 2}, {'UpperBoundOcc': 2, 'LowerBoundNeg': 0, 'UpperBoundNeg': 1, 'LowerBoundPos': 0, 'UpperBoundPos': 0}]
%  efficiency constraints: False
%  optimization strategy: 1  (minimize inputs then minimize gates)

% the tissue data, a tissue ID followed by either "cancer" or "healthy"
tissue(1,healthy). tissue(2,healthy). tissue(3,cancer).

% for binding variables we need the "is_tissue_id" predicate
is_tissue_id(X) :- tissue(X,Y).

% the miRNA data, a tissue ID and miRNA ID followed by either "high" or "low"
data(1,g1,high). data(1,g2,high). data(1,g3,low). data(2,g1,low). data(2,g2,low). data(2,g3,high). data(3,g1,low).
data(3,g2,high). data(3,g3,low).

% for binding variables we need the "is_miRNA" predicate
is_mirna(Y) :- data(X,Y,Z).



%%%% Classifier Structure %%%%
% definition of gate types in terms of upper bounds on number of inputs
is_gate_type(type1).
upper_bound_pos_inputs(type1, 2).
upper_bound_neg_inputs(type1, 0).
lower_bound_pos_inputs(type1, 0).
lower_bound_neg_inputs(type1, 0).
upper_bound_gate_occurence(type1, 1).

is_gate_type(type2).
upper_bound_pos_inputs(type2, 0).
upper_bound_neg_inputs(type2, 1).
lower_bound_pos_inputs(type2, 0).
lower_bound_neg_inputs(type2, 0).
upper_bound_gate_occurence(type2, 2).


% each input may be positive or negative
is_sign(positive). is_sign(negative).

% upper bound for total number of inputs
upper_bound_inputs(10).


%%%% Decisions %%%%
% First decision: the exact number of gates
1 {number_of_gates(1..2)} 1.
is_integer(1..2).
is_gate_id(GateID) :- number_of_gates(X), is_integer(GateID), GateID<=X.

% Second decision: each gates is assigned a gate type
1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).

% efficiency OFF: unrestricted miRNAs for inputs
% Third decision: each gate is assigned a number of inputs
X {gate_input(GateID, positive, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).
X {gate_input(GateID, negative, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).


%%%% Constraints %%%%
% each gate must have at least one input
1 {gate_input(GateID, Sign, MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).

% inputs must be unique for a classifer
{gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_gate_id(GateID)} 1 :- is_mirna(MiRNA).

% the total number of inputs is bounded
{gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} X :- upper_bound_inputs(X).

% the number of occurences of a gate type is bounded
{gate_type(GateID,GateType): is_gate_id(GateID)} X :- upper_bound_gate_occurence(GateType,X).

% gates are disjunctive (one active input suffices to activate gate)
gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high).
gate_fires(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low).

% the classifier is a conjunction of all gate evaluations.
classifier(TissueID,healthy) :- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID).
classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID).

% the classifier must agree with the tissue data.
:- tissue(TissueID,healthy), classifier(TissueID,cancer).
:- tissue(TissueID,cancer),  classifier(TissueID,healthy).

% optimization setup 2: first number of inputs then number of gates.
#minimize{ 1@1,MiRNA: gate_input(GateID,Sign,MiRNA) }.
#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }.

#show gate_input/3.