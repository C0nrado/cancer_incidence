import pandas as pd
import sys
from resources.utils import summary_dataset
import pickle

class WrongInput(Exception):
    def __init__(self, error):
        pass

def read_dataset():
    """This function returns the data set from the provided buffer when running the script."""

    if len(sys.argv) <= 1:
        raise WrongInput('Missing Buffer path')
    else:
        try:
            # reading buffer path
            buffer = sys.argv[1]

            df = pd.read_fwf(buffer)
        
        except:
            raise WrongInput('Incorrect path.')
    
    return df

col_names = {'Ident':'ID',
             'Grupo':'Group',
             'Idade':'Age'}

group_values = {1: 'FP',
                2: 'FN',
                3: 'N',
                4: 'P'}

df = read_dataset() \
        .rename(col_names, axis=1) \
        .replace({'Group':group_values})

print(summary_dataset(df))
pickle.dump(df, open('cancer_dataset.pkl', 'wb'))