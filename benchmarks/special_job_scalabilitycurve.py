
import os
import matplotlib
import matplotlib.pyplot
import matplotlib.cm


import numpy    
import scipy.interpolate

import interfaces



def run():

    Folder = "50x10_50x10000_1x1_kobi_kobi_feasible_30m"
    DataArray = interfaces.files.read_benchmark_folder(Folder)
    
    Title = None

    FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT = Folder.split('_')

    X,Y,T = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray, Key='time')
            
    T_new = [-100 if numpy.isnan(x) else x for x in T]
    T = T_new

    figure = matplotlib.pyplot.figure()
    
    ax = figure.add_subplot(111)
    ax.set_ylim([-200, 2000])

    matplotlib.pyplot.yticks([-100,0,300,600,900,1200,1500,1800], ['timeout','0','5m','10m','15m','20m','25m','30m'])
    
               

    
    matplotlib.pyplot.xlabel('miRNAs')
    matplotlib.pyplot.ylabel('time')
    matplotlib.pyplot.plot(Y,T,'ro', color="black", marker=".")

    figure.suptitle('Scalability (50 tissues)')

    fname_figure = os.path.join('plots', 'scalability_'+Folder+'.pdf')
    figure.savefig(fname_figure)
    interfaces.plotting.crop_pdf(fname_figure)
    
    print(' created {X}'.format(X=fname_figure))




if __name__=="__main__":
    run()




