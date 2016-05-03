

Cancer classification based on miRNA profiles using ASP

1. Background
- kill signal for cancer cells based on miRNA fingerprint


2. Mathematical Biological constraints
- Less than 10 inputs in total
- no more than 6 inputs attached to the AND gate
- no more than 3 inputs atttached to any OR gate
- no NOT gates attacched to an OR gate
- no more than 2 OR gates
- no more than 4 NOT gates


3. ASP encoding
- data
   - tissue(1, healthy).
   - data(1, g1, low).

- for variable binding:
   - is_miRNA(Y) :-data(X,Y,Z).
   - is_gate_type(1..2).
   - is_sign(positive).

- classifier constraints
   - upper_bound_positive_inputs(gatetype1, 0)
   - upper_bound


4. computer experiments
   - complete truth tables
   - generate classifier
      - select rows
   - generate random matrix
      - 
   - random truth tables with three parameters: number rows, number columns, % healthy -> Zeit first result, Zeit all results, number all results


5. Heike's Slices


TODO
renames:
   upper_bound_pos_inputs(1, 3). -> upper_bound_positive_inputs(gatetype1, 0).
   is_gate_type(1..2). -> is_GateType(GateType1). is_GateType(GateType1).
   is_sign(positive). -> is_Sign(positive).
   upper_bound_total_inputs(10). -> upper_bound_inputs(10).
   is_gate_id(GateID) -> is_GateID(GateID)
   feasible_pos_miRNA(MiRNA) -> feasible_positive_input(MiRNA)
   feasible_neg_miRNA(MiRNA) -> feasible_negative_input(MiRNA)
   
   
   
   
   
   
   
   
   
