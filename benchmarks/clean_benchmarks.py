

import os

if __name__=='__main__':
    print('\nwelcome to clean_benchmarks.py')
    counter = 0
    
    for folder in os.listdir('benchmarks'):
        for fname in os.listdir(os.path.join('benchmarks',folder)):
            if not fname.endswith('.result'):
                os.remove(os.path.join('benchmarks',folder,fname))
                counter+=1

    print(' removed {X} files.'.format(X=counter))
