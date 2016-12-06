

import numpy

import re

SECONDS_PATTERN = re.compile("^[0-9]+\.[0-9]+s$") # example: "0.010s"

def time2int(Time):
    if Time=='-1':
        return -1
    
    if not SECONDS_PATTERN.match(Time):
        print(' what time is it: {X}'.format(X=Time))
        raise Exception
    else:
        return float(Time.replace('s',''))
    


def convert_data_to_X1d_Y1d_Z1d(DataArray):

    X,Y,Z = [],[],[]
    
    for pos, data in DataArray.items():
        x,y = pos
        X.append(x)
        Y.append(y)
        Z.append(time2int(data['time']))

    return X,Y,Z


def convert_data_to_X1d_Y1d_Z2d(DataArray):
    X,Y,dummy = convert_data_to_X1d_Y1d_Z1d(DataArray)

    Z = numpy.zeros(shape=(max(X)+1, max(Y)+1))

    for x,y,z in zip(X,Y,dummy):
        Z[x,y] = z
        
    return X,Y,Z
    
    
