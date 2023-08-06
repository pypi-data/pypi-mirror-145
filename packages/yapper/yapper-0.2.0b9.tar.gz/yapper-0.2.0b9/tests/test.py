#%%
import docstring_parser

test = docstring_parser.parse('''

    Parameters
    ----------
    param_a
        A param
    
    Examples
    --------
    
    $\\neq$

''')

print(test)