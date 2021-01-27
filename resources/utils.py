import pandas as pd
import numpy as np

def summary_dataset(df):

    def add_line(string, values, line_pattern='{:<15s}{:>20s}\n'):
        for value in values:
            assert isinstance(value, str)
        
        return string + line_pattern.format(*values)
    
    def multiline(string, width=30, sep=' '):
        idx = string.rfind(sep, 0, width)
        out = []
        while len(string) > width:
            out.append(string[:idx])
            string = string[idx+1:]
            idx = string.rfind(sep, 0, width)
        
        out.append(string)
        return len(out), out

    fill_line = lambda x, width: x + '-'*width + '\n'
    default_width = 35
    out = ''
    out = fill_line(out, default_width)
    out += 'Data Set Summary'.center(35) + '\n'
    out = fill_line(out, default_width)

    if isinstance(df.index, pd.PeriodIndex) or isinstance(df.index, pd.DatetimeIndex):
        out = add_line(out, ('Starts at', str(df.index.min())))
        out = add_line(out, ('Ends at', str(df.index.max())))
        out = add_line(out, ('Type', str(df.index.dtype)))
    
    out = add_line(out, ('Entries', str(len(df))))
    
    n_lines, fields_lines = multiline(', '.join(df.columns), 20)
    
    for values in zip(['Fields'+' ('+str(len(df.columns))+')']+['']*(n_lines-1), fields_lines):
        out = add_line(out, values)
    
    out = add_line(out, ('NULL ', str(df.isnull().sum().sum())))
    out = add_line(out, ('Memory[KB]', str(round(df.memory_usage().sum()/(2**10),1))))
    
    out = fill_line(out, default_width)
    out += 'Data Types'.center(35) + '\n'
    out = fill_line(out, default_width)

    for values in (tuple(d.split()) for d in df.dtypes.to_string().split('\n')):
        out = add_line(out, values)
    
    # Statistics columh
    
    col2_body = df.describe().round(1).to_string()
    line_width = len(col2_body.split('\n')[0])
    
    col2 = '' 
    col2 = fill_line(col2, line_width)
    col2 += 'Statistics'.center(line_width) + '\n'
    col2 = fill_line(col2, line_width)
    col2 += col2_body
    out = out.split('\n')
    col2 = col2.split('\n')


    final = [line1 + '|'.center(5) + line2
                    for line1, line2 in zip(out, col2 + ['']*(len(out) - len(col2) -1))]
    final_width = len(final[0])
    
    out = '='*(final_width) + '\n'
    out += '\n'.join(final) + '\n'
    out += '-'*final_width + '\n'
    out += '='*(final_width)

    return out