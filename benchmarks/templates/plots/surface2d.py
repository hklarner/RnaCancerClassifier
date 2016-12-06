

import os
import matplotlib
import matplotlib.pyplot
import matplotlib.cm


import numpy    
import scipy.interpolate

import interfaces
              
              


def run(Benchmark, DataArray):

    FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT = Benchmark.split('_')
    FROM_X, FROM_Y = map(int,FROM.split('x'))
    TO_X, TO_Y = map(int,TO.split('x'))
    SKIP_X, SKIP_Y = map(int,SKIP.split('x'))

    fname_figure = os.path.join('plots', Benchmark+'_surface2D.pdf')


    X,Y,Z = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray)

    # matplotlib stuff
    
    figure = matplotlib.pyplot.figure()
    
    ax = figure.add_subplot(111, aspect='equal')
    ax.axis([min(X)-1., max(X)+1., min(Y)-1., max(Y)+1.])

    cmap = matplotlib.cm.cool
    cmap.set_over('black')
    cmap.set_under('white')

    norm = matplotlib.colors.Normalize(vmin=0., vmax=max(Z))
    scalarmap = matplotlib.cm.ScalarMappable(norm, cmap)

    
    #print help(cmap)
    #return
    #print map(cmap,sorted(Z))
    
    dx = SKIP_X-1.
    dy = SKIP_Y-1.
    for x, y, z in zip(X,Y,Z):
        ax.add_artist(matplotlib.patches.Rectangle(xy=(x-dx/2., y-dx/2.), color=scalarmap.to_rgba(z), width=dx, height=dy))

    matplotlib.pyplot.scatter(X, Y, c=Z, edgecolors='none', marker='s')

    
    cbar = matplotlib.pyplot.colorbar(orientation='vertical')
    cbar.set_cmap(cmap)
    cbar.update_normal(mappable=ax)
    cbar.set_label('time (sec)')
    
    
    matplotlib.pyplot.xlabel('tissues')
    matplotlib.pyplot.ylabel('miRNAs')



    
    title = ['Objective: {X}'.format(X=OBJECTIVE)]
    if CLASSIFIER_ANNOTATION == CLASSIFIER_SOLUTION:
        title+= ['Classifier: {X}'.format(X=CLASSIFIER_ANNOTATION)]
    else:
        title+= ['Classifier (Annot): {X}'.format(X=CLASSIFIER_ANNOTATION),
                 'Classifier (Soltn): {X}'.format(X=CLASSIFIER_SOLUTION)]
    title+= ['Timeout: {X}'.format(X=TIMEOUT)]

    figure.suptitle(' / '.join(title))

    figure.savefig(fname_figure)
    
    

