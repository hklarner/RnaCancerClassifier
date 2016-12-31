

import os
import matplotlib
import matplotlib.pyplot
import matplotlib.cm


import numpy    
import scipy.interpolate

import interfaces


def run(Type, Folder, DataArray, Title=None):

    if Type=='benchmark':
        FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT = Folder.split('_')
        X,Y,Z = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray, Key='time')
    else:
        FROM, TO, SKIP, CLASSIFIER_ANNOTATION, CLASSIFIER_SOLUTION, OBJECTIVE, TIMEOUT, VALIDATION = Folder.split('_')
        X,Y,Z = interfaces.plotting.convert_data_to_X1d_Y1d_Z1d(DataArray, Key='error')
        
    FROM_X, FROM_Y = map(int,FROM.split('x'))
    TO_X, TO_Y = map(int,TO.split('x'))
    SKIP_X, SKIP_Y = map(int,SKIP.split('x'))

    # here goes matplotlib
    
    figure = matplotlib.pyplot.figure()
    
    ax = figure.add_subplot(1,1,1, aspect='equal')
    ax.axis([min(X)-1., max(X)+1., min(Y)-1., max(Y)+1.])

    cmap = matplotlib.cm.cool
    cmap.set_over('black')
    cmap.set_under('white')

    norm = matplotlib.colors.Normalize(vmin=0., vmax=max(Z))
    scalarmap = matplotlib.cm.ScalarMappable(norm, cmap)
    
    dx = SKIP_X-2.
    dy = SKIP_Y-2.
    for x, y, z in zip(X,Y,Z):

        if Type=='benchmark':

            found_solution = DataArray[(x,y)]['solution']!=None
            timed_out      = DataArray[(x,y)]['time']==None

            if found_solution and timed_out:
                print(' how is found_solution and timed_out possible?')
                raise Exception

            if found_solution and not timed_out:
                patch = matplotlib.patches.Rectangle(xy=(x-dx/2., y-dx/2.), color=scalarmap.to_rgba(z), width=dx, height=dy)


            if not found_solution and timed_out:
                patch = matplotlib.patches.Rectangle(xy=(x-dx/2., y-dx/2.), color='white', width=dx, height=dy)#, angle=45)
                patch.set_edgecolor('black')


            if not found_solution and not timed_out:
                patch = matplotlib.patches.Rectangle(xy=(x-dx/2., y-dx/2.), color=scalarmap.to_rgba(z), width=dx, height=dy)
                patch.set_edgecolor('black')                    
        
        elif Type=='crossvalidation':
            patch = matplotlib.patches.Rectangle(xy=(x-dx/2., y-dx/2.), color=scalarmap.to_rgba(z), width=dx, height=dy)
            
            if (z==0 or z==1):
                pass #patch.set_edgecolor('black')

        ax.add_artist(patch)

    matplotlib.pyplot.scatter(X, Y, c=Z, edgecolors='none', marker='s')

    
    cbar = matplotlib.pyplot.colorbar(orientation='vertical')
    cbar.set_cmap(cmap)
    cbar.update_normal(mappable=ax)

    if Type=='benchmark': 
        cbar.set_label('time (sec)')
    else:
        cbar.set_label('generalization error')
    
    matplotlib.pyplot.xlabel('tissues')
    matplotlib.pyplot.ylabel('miRNAs')


    if not Title:
        title = ['Objective: {X}'.format(X=OBJECTIVE)]

        if CLASSIFIER_ANNOTATION == CLASSIFIER_SOLUTION:
            title+= ['Classifiers: {X}'.format(X=CLASSIFIER_ANNOTATION)]
        else:
            title+= ['Classifier (Annot): {X}'.format(X=CLASSIFIER_ANNOTATION),
                     'Classifier (Soltn): {X}'.format(X=CLASSIFIER_SOLUTION)]

        title+= ['Timeout: {X}'.format(X=TIMEOUT)]
        figure.suptitle(' / '.join(title))

    else:
        figure.suptitle(Title)

    fname_figure = os.path.join('plots', Type, Folder+'_surface2d.pdf')
    figure.savefig(fname_figure)

    interfaces.plotting.crop_pdf(fname_figure)
    print(' created {X}'.format(X=fname_figure))
    
    

