
import random

import sys
sys.path.insert(0, '../')
import classifier as CLASSIFIER_SCRIPT

import potassco
import interfaces


def create_gate_instance(GateType, MiRNAs):
    
    if GateType['UpperBoundPos']<=0 and GateType['UpperBoundNeg']<=0:
        print(' invalid gate type sepcification: impossible to assign inputs.')
        raise Exception

    number_pos_inputs, number_neg_inputs, safety = 0, 0, 0
    while True:
        safety+=1
        if safety>1000:
            return None
            print('GateType: {x}'.format(x=GateType))
            print('MiRNAs:   {x}'.format(x=MiRNAs))
            return None

        number_pos_inputs = random.randint(GateType['LowerBoundPos'],GateType['UpperBoundPos'])
        number_neg_inputs = random.randint(GateType['LowerBoundNeg'],GateType['UpperBoundNeg'])

        if number_pos_inputs==0 and number_neg_inputs==0:
            continue

        if number_pos_inputs + number_neg_inputs > len(MiRNAs):
            continue

        pos_inputs = random.sample(MiRNAs, number_pos_inputs)
        for x in pos_inputs: MiRNAs.remove(x)
        neg_inputs = random.sample(MiRNAs, number_neg_inputs)
        for x in neg_inputs: MiRNAs.remove(x)

        
        gate_input_str = 'gate_input({{ID}},{SIGN},{RNA})'

        gate = [gate_input_str.format(SIGN='positive',RNA=x) for x in pos_inputs]
        gate+= [gate_input_str.format(SIGN='negative',RNA=x) for x in neg_inputs]
        gate = ' '.join(sorted(gate))

        return gate
        

def gate_generator(GateTypes, MaxMiRNAs):
    GateTypes = [x for x in GateTypes if x['UpperBoundOcc']>0]
    if not GateTypes:
        print(' UpperBoundOcc=0 for all gate types, impossible to construct classifier.')
        raise Exception
    
    gate_type_ids = range(len(GateTypes))
    occurences = dict((i,0) for i in gate_type_ids)
    allowed_gate_types = gate_type_ids

    mirnas = range(1,MaxMiRNAs+1)

    safety = 0
    while allowed_gate_types:
        safety+= 1
        if safety>100:
            break

        gate_type_id = random.choice(allowed_gate_types)

        gate = create_gate_instance(GateTypes[gate_type_id], mirnas)
        
        if gate:
            if occurences[gate_type_id]>=GateTypes[gate_type_id]['UpperBoundOcc']:
                allowed_gate_types.remove(gate_id)

            yield gate
        
    

def create_random_classifier(Template, MaxMiRNAs):
    params = interfaces.templates.read_classifier(Template)

    lower_gates = max(1,params['LowerBoundGates'])
    upper_gates = max(1,params['UpperBoundGates'])
    
    target_number_gates  = random.randint(lower_gates,upper_gates)
    target_number_gates = max(1,target_number_gates)
    current_number_gates  = 0
    current_number_inputs = 0
    result = []

    for gate in gate_generator(params['GateTypes'], MaxMiRNAs):
        if current_number_gates >= target_number_gates:
            break
        
        current_number_inputs+= gate.count('gate_input')
        if current_number_inputs>params['UpperBoundInputs']:
            if not result:
                result+=[gate]
            break

        if gate in result:
            print(' generated duplicate gate!')
            raise Exception

        result+=[gate]
        current_number_gates+= 1
        
        
    if not result:
        print(' generated empty classifier!')
        raise Exception

    result = ' '.join(x.format(ID=i) for i, x in enumerate(result))
    
    return result
    
    

def gateinputs2function(GateInputs):
    with interfaces.files.nostdout():
        function = CLASSIFIER_SCRIPT.gateinputs2function(GateInputs)

    def wrapper(SampleDict):
        SampleDict['Annots'] = '1'

        false_pos, false_neg, malfunction = function(SampleDict)

        if false_neg:
            
            return 0

        return 1

    return wrapper


        


                                        
