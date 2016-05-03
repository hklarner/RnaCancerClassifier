
% ASP constraints for computing a classifier (in this case a Boolean Function),
% that agrees with given tissue data (either cancerous or healthy) and
% and satisfies certain structural constraints.
% Note: a classifier is the conjunction of disjunctive gates (CNF)
% written by K. Becker and H. Klarner, March 2016, FU Berlin.

% InputFile = toy.csv
%  upper bound on inputs: 2
%  upper bound on gates: 2
%  gate types: [{'UpperBoundOcc': 1, 'LowerBoundNeg': 0, 'UpperBoundNeg': 0, 'LowerBoundPos': 0, 'UpperBoundPos': 1}, {'UpperBoundOcc': 2, 'LowerBoundNeg': 0, 'UpperBoundNeg': 1, 'LowerBoundPos': 0, 'UpperBoundPos': 0}]
%  efficiency constraints: True
%  optimization strategy: 2  (minimize inputs then minimize gates)

% the tissue data, a tissue ID followed by either "cancer" or "healthy"
tissue(1,healthy). tissue(2,healthy). tissue(3,cancer).

% for binding variables we need the "is_tissue_id" predicate
is_tissue_id(X) :- tissue(X,Y).

% the miRNA data, a tissue ID and miRNA ID followed by either "high" or "low"
data(1,g1,high). data(1,g2,high). data(1,g3,low). data(2,g1,low). data(2,g2,low). data(2,g3,high). data(3,g1,low).
data(3,g2,high). data(3,g3,low).

% for binding variables we need the "is_miRNA" predicate
is_miRNA(Y) :- data(X,Y,Z).



%%%% Classifier Structure %%%%
% definition of gate types in terms of upper bounds on number of inputs
is_gate_type(1..2).
upper_bound_pos_inputs(1, 1). % GateType_1
upper_bound_neg_inputs(1, 0). % GateType_1
lower_bound_pos_inputs(1, 0). % GateType_1
lower_bound_neg_inputs(1, 0). % GateType_1
upper_bound_gate_type(1, 1). % GateType_1
upper_bound_pos_inputs(2, 0). % GateType_2
upper_bound_neg_inputs(2, 1). % GateType_2
lower_bound_pos_inputs(2, 0). % GateType_2
lower_bound_neg_inputs(2, 0). % GateType_2
upper_bound_gate_type(2, 2). % GateType_2

% each input may be positive or negative
is_sign(positive). is_sign(negative).

% upper bound for total number of inputs
upper_bound_total_inputs(2).


%%%% Decisions %%%%
% First decision: the exact number of gates
1 {number_of_gates(1..2)} 1.
is_integer(1..2).
is_gate_id(GateID) :- number_of_gates(X), is_integer(GateID), GateID<=X.

% Second decision: each gates is assigned a gate type
1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).

% efficiency ON: restrict miRNA for inputs (requires the assumptionin that number of miRNAs is minimal)
feasible_pos_miRNA(MiRNA) :- is_miRNA(MiRNA), data(TissueID, MiRNA, high), tissue(TissueID,cancer).
feasible_neg_miRNA(MiRNA) :- is_miRNA(MiRNA), data(TissueID, MiRNA, low),  tissue(TissueID,cancer).

% Third decision: each gate is assigned a number of inputs
X {gate_input(GateID, positive, MiRNA): feasible_pos_miRNA(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).
X {gate_input(GateID, negative, MiRNA): feasible_neg_miRNA(MiRNA)} Y :- is_gate_id(GateID), gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).


%%%% Constraints %%%%
% each gate must have at least one input
1 {gate_input(GateID, Sign, MiRNA): is_sign(Sign), is_miRNA(MiRNA)} :- is_gate_id(GateID).

% the total number of inputs is bounded
{gate_input(GateID, Sign, MiRNA): is_gate_id(GateID), is_sign(Sign), is_miRNA(MiRNA)} X :- upper_bound_total_inputs(X).

% the number of gates of a gate type is bounded
{gate_type(GateID,T): is_gate_type(T), is_gate_id(GateID)} X :- upper_bound_gate_type(T,X).

% gates are disjunctive (one active input suffices to activate gate)
gate_evaluation(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high).
gate_evaluation(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low).

% inputs must not be positive and negative in the same gate
:- gate_input(GateID,positive,MiRNA), gate_input(GateID,negative,MiRNA).

% an input cannot be used for two different gates
:- gate_input(X,_,MiRNA), gate_input(Y,_,MiRNA), X<Y.

% the classifier is a conjunction of all gate evaluations.
classifier(TissueID, healthy) :- not gate_evaluation(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID).
classifier(TissueID, cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID).

% the classifier mus agree with the tissue data.
:- tissue(TissueID,healthy), classifier(TissueID,cancer).
:- tissue(TissueID,cancer),  classifier(TissueID,healthy).

% optimization setup 2: first number of inputs then number of gates.
#minimize{ 1@1,MiRNA: gate_input(GateID,Sign,MiRNA) }.
#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }.

#show gate_input/3.
