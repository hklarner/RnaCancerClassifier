

import os
import matplotlib
import matplotlib.pyplot
import matplotlib.cm


import numpy    
import scipy.interpolate

import interfaces


def run(Folder, DataArray, Title=None):

    FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT, VALIDATION = Folder.split('_')

    X,Y,E = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray, Key='error')
    X,Y,T = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray, Key='time')

    figure = matplotlib.pyplot.figure()
    
    ax = figure.add_subplot(111)
    ax.set_xlim([0, 100])
    matplotlib.pyplot.xlabel('time (sec)')
    matplotlib.pyplot.ylabel('error (percent)')
    matplotlib.pyplot.plot(T,E,'ro')

    fname_figure = os.path.join('plots', 'error_vs_time_'+Folder+'.pdf')
    figure.savefig(fname_figure)
    interfaces.plotting.crop_pdf(fname_figure)
    
    print(' created {X}'.format(X=fname_figure))
    
    
    

