
import interfaces

import numpy
import subprocess
import re
TIME_PATTERN = re.compile("^[0-9]+[\.]?[0-9]*(?:m|s)$") # example: "0.010s" or "5m"


def time2int(Time):
    if TIME_PATTERN.match(Time):
        if 'm' in Time:
            return 60*float(Time.replace('m',''))
        else:
            return float(Time.replace('s',''))
    
        
    else:
        print(' what time is it: {X}'.format(X=Time))
        raise Exception
        

def crop_pdf(Fname):
    subprocess.check_output(['pdfcrop',Fname,Fname])


def convert_data_to_X1d_Y1d_Z1d(DataArray, Key):

    X,Y,Z = [],[],[]
    
    for pos, data in DataArray.items():
        x,y = pos
        X.append(x)
        Y.append(y)

        if Key=='time':
            if data[Key]==None:
                Z.append( numpy.nan )
            elif TIME_PATTERN.match(data[Key]):
                Z.append(time2int(data[Key]))
            else:
                Z.append(float(data[Key]))
        else:
            Z.append(float(data[Key]))

    return X,Y,Z


def convert_data_to_X1d_Y1d_Z2d(DataArray, Key):
    X,Y,dummy = convert_data_to_X1d_Y1d_Z1d(DataArray, Key)

    Z = numpy.zeros(shape=(max(X)+1, max(Y)+1))

    for x,y,z in zip(X,Y,dummy):
        Z[x,y] = z
        
    return X,Y,Z
    
    
