

import sys
import os
import importlib

import networkx
import interfaces

import templates.plots.error_vs_time


def gate_input2triple(GateInput):
    return GateInput[11:-1].split(',')

def gate_input2mirna(GateInput):
    sign, mirna = gate_input2triple(GateInput)[1:]
    return "_".join([mirna, sign])

def solution2digraph(Solution):
    g = networkx.DiGraph()
    for x in Solution:
        gate, sign, mirna = gate_input2triple(x)

        if not gate in g:
            g.add_node(gate)
            g.node[gate]["label"] = ""

        if not mirna in g:
            g.add_node(mirna, label=mirna)

        g.add_edge(mirna,gate, label=sign)

    return g


def digraph2solution(Digraph):
    inputs = []
    for x,y,data in Digraph.edges(data=True):

        gateid = str(y)
        mirna = Digraph.node[x]["label"]
        sign = data["label"]
        
        inputs.append("gate_input({x},{y},{z})".format(x=gateid, y=mirna, z=sign))

    return " ".join(inputs)


def labels_are_equal(X,Y):
    return X["label"] == Y["label"]

def solutions2classes(Solutions):
    classes = []
    graphs = [solution2digraph(x) for x in Solutions]

    
    for G1 in graphs:

        hit = False
        for G2 in classes:
            if networkx.is_isomorphic(G1, G2, node_match=labels_are_equal, edge_match=labels_are_equal):
                hit = True
                break
            
        if not hit:
            classes.append(G1)

    return classes
    

    

def run():

    lines = open("all_results_C2_relaxedconstraints.txt", "r").read()
    result = ["input: all_results_C2_relaxedconstraints.txt"]
    
    solutions = interfaces.potassco.output2gateids(lines)
    solutions = [x.split() for x in solutions]
    
    mirnas = set([])
    for sol in solutions:
        new = tuple(sorted([gate_input2mirna(gate) for gate in sol]))
        mirnas.add(new)

    result+=["answer sets: %i"%len(solutions)]
    result+=[""]
    
    result+=["mirna-sets: %i"%len(mirnas)]
    for i,mirna in enumerate(mirnas):
        result+=[" {x}: {y}".format(x=i+1,y=", ".join(sorted(mirna)))]

    result+=[""]
    
                 
                 
    classes = solutions2classes(solutions)
    result+=["classes: %i"%len(classes)]
    
    for i,x in enumerate(classes):
        result+=[" {x}: {y}".format(x=i+1,y=digraph2solution(x))]

    with open("iso_classes_for_C2_relaxedconstraints.txt", "w") as resfile:
        resfile.write("\n".join(result))


if __name__=="__main__":
    run()
