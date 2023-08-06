from collections.abc import Sequence, Callable
from inspect import signature

def reduce_args(func: Callable, args: Sequence=None, arg_index: int=None) -> Callable:
    '''
    Returns a function that has been reduced to a single argument.
    ----------        
    Parameters:
    ----
        func (Callable): Python function to be reduced.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
    ----
    Returns:
    ----
        reduced_func (Callable): A function that has been reduced to a single argument.
    '''
    if len(signature(func).parameters) == 1: #If function has only one parameter, return function itself.
        return func
    else: #If function has more than one parameter, return a function that has been reduced to a single argument.
        if not isinstance(args, Sequence):
            raise ValueError('function passed has more than one input, then args must be specified as Sequence.')
        if arg_index is None:
            raise ValueError('function passed has more than one input, then arg_index must be specified.')
        def reduced_func(x):
            args[arg_index] = x
            return func(*args)
        return reduced_func