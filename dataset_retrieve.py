import pandas as pd
from os.path import exists
import sys
from resources.utils import summary_dataset
import pickle

class WrongInput(Exception):
    def __init__(self, error):
        pass

def parse_argv():
    if len(sys.argv) <= 1:
        raise WrongInput('Missing Buffer path')
    else:
        try:
            string = ' '.join(sys.argv[1:]).split('-')
            split_argv = [tuple(arg.strip().split(' ')) for arg in string if arg != '']
            args = dict(map(lambda x: (x[0], True) if len(x) == 1 else x, split_argv))
            if not args.get('force'):
                args['force'] = False

        except:
            raise WrongInput('Something went wrong in the given input.')
    
    if len(set(args.keys()) - set(['i', 'O', 'force'])) > 0:
        raise WrongInput('Incorrect inputs.')
    
    return args

def read_dataset():
    """This function returns the data set from the provided buffer when running the script."""

    # reading buffer path
    try:
        buffer = args['i']
        df = pd.read_fwf(buffer)
    except:
        raise WrongInput('Missing/Wrong input path.')
   
    return df

def output(df):

    def save_file():
        pickle.dump(df, open(args['O'], 'wb'))
        print('Data set saved in %s'%args['O'])

    # setting output file
    if 'O' not in args.keys():
        args['O'] = './output.pkl'
    
    if exists(args['O']):
        if not args['force']:
            raise WrongInput('File %s already exists.'%args['O']) 
    
    save_file()
        
args = parse_argv()
df = read_dataset()
output(df)
print(summary_dataset(df))