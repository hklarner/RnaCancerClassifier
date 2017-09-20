
% ASP constraints for computing a miRNA cancer classifier
% that agrees with given tissue data and satisfies given structural constraints.
% note: A classifier is a Boolean expression in conjunctive form.
% the homepage of the project is https://github.com/hklarner/RnaCancerClassifier.
% written by K. Becker and H. Klarner, March 2016, FU Berlin.

% InputFile = toy.csv
%  efficiency constraints: False
%  optimization strategy: 1  (minimize gates then minimize inputs)


%%% The tissue data
tissue(1,healthy). tissue(2,healthy). tissue(3,cancer).

%%% The miRNA data
data(1,g1,high). data(1,g2,high). data(1,g3,low). data(2,g1,low). data(2,g2,low). data(2,g3,high). data(3,g1,low).
data(3,g2,high). data(3,g3,low).


%%% User Input
lower_bound_inputs(1).
upper_bound_inputs(10).
lower_bound_gates(1).
upper_bound_gates(2).

% gate type 1.
is_gate_type(1).
upper_bound_pos_inputs(1, 2).
upper_bound_neg_inputs(1, 0).
lower_bound_pos_inputs(1, 0).
lower_bound_neg_inputs(1, 0).
upper_bound_gate_occurence(1, 1).

% gate type 2.
is_gate_type(2).
upper_bound_pos_inputs(2, 0).
upper_bound_neg_inputs(2, 1).
lower_bound_pos_inputs(2, 0).
lower_bound_neg_inputs(2, 0).
upper_bound_gate_occurence(2, 2).

% binding of variables
is_tissue_id(X) :- tissue(X,Y).
is_mirna(Y) :- data(X,Y,Z).
is_sign(positive). is_sign(negative).


%%% Constraints
% number of gates
1 {number_of_gates(X..Y)} 1 :- lower_bound_gates(X), upper_bound_gates(Y).
is_gate_id(1..X) :- number_of_gates(X).

% assignment of gate types
1 {gate_type(GateID, X): is_gate_type(X)} 1 :- is_gate_id(GateID).

% inputs for gates (EfficiencyConstraint=False)
X {gate_input(GateID, positive, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_pos_inputs(GateType, X), upper_bound_pos_inputs(GateType, Y).
X {gate_input(GateID, negative, MiRNA): is_mirna(MiRNA)} Y :- gate_type(GateID, GateType), lower_bound_neg_inputs(GateType, X), upper_bound_neg_inputs(GateType, Y).

% at least one input for each gate
1 {gate_input(GateID,Sign,MiRNA): is_sign(Sign), is_mirna(MiRNA)} :- is_gate_id(GateID).

% inputs must be unique for gates
{gate_input(GateID,Sign,MiRNA): is_sign(Sign)} 1 :- is_mirna(MiRNA), is_gate_id(GateID).

% number of inputs is bounded
X {gate_input(GateID,Sign,MiRNA): is_gate_id(GateID), is_sign(Sign), is_mirna(MiRNA)} Y :- lower_bound_inputs(X), upper_bound_inputs(Y).

% occurences of gate types is bounded
{gate_type(GateID,GateType): is_gate_id(GateID)} X :- upper_bound_gate_occurence(GateType,X).

% gates fire condition
gate_fires(GateID,TissueID) :- gate_input(GateID,positive,MiRNA), data(TissueID,MiRNA,high).
gate_fires(GateID,TissueID) :- gate_input(GateID,negative,MiRNA), data(TissueID,MiRNA,low).

% prediction of classifier
classifier(TissueID,healthy) :- not gate_fires(GateID, TissueID), is_gate_id(GateID), is_tissue_id(TissueID).
classifier(TissueID,cancer) :- not classifier(TissueID, healthy), is_tissue_id(TissueID).

% consistency of classifier and data (PerfectClassifier=True)
:- tissue(TissueID,healthy), classifier(TissueID,cancer).
:- tissue(TissueID,cancer),  classifier(TissueID,healthy).


%%% Breaking symmetries
% gate id symmetries
GateType1 <= GateType2 :- gate_type(GateID1, GateType1), gate_type(GateID2, GateType2), GateID1 <= GateID2.


% optimization setup 2: first number of inputs then number of gates.
#minimize{ 1@1,(GateID,MiRNA): gate_input(GateID,Sign,MiRNA) }.
#minimize{ 1@2,GateID:gate_input(GateID,Sign,MiRNA) }.

#show gate_input/3.