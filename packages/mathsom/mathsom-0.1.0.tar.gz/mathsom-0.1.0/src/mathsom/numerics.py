from collections.abc import Sequence, Callable
from .auxfuncs import reduce_args
from itertools import accumulate, repeat


def differentiate(func: Callable, arg: float, args: Sequence=None, argument_index: int=None, step: float=0.0000001) -> float:
    '''
    Numeric function derivative.
    ----
    Parameters:
    ----
        func (Callable): Python objective function to be differentiated.
        arg (float): Number where function will be differentiated. If function contains many arguments, use func_inputs with partial_argument_index parameters instead. The default is None. Example: f'(2) -> arg = 2.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
        step (float): Optional. Step size. Default is 0.0000001.
    ----
    Returns:
    ----
        slope (float).'''
    func = reduce_args(func, args, argument_index)    
    
    y_fwd_step = func(arg + step)
    y_back_step = func(arg - step)
    slope = (y_fwd_step - y_back_step) / (2.0 * step)
    return slope

def integrate(func: Callable, x_start: float, x_end: float, args: Sequence=None, argument_index: int=None, n_steps: int=10_000):
    '''
    Numeric function integration with Trapezoidal rule.
    ----
    Parameters:
    ----
        func (Callable): Python objective function to be integrated.
        x_start (float): Start of integration interval.
        x_end (float): End of integration interval.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
        n_steps (int): Optional. Number of steps. Default is 10_000.
    ----        
    Returns:
    ----
        integration_value (float)
    '''
    func = reduce_args(func, args, argument_index)
    step_length = (x_end - x_start) / n_steps
    xs = accumulate(repeat(step_length, n_steps - 2), initial = x_start + step_length)
    area = sum(map(func, xs))
    area = area * 2.0 + func(x_start) + func(x_end)
    return area * step_length / 2.0
