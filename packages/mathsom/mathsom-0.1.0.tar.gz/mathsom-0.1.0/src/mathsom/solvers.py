from collections.abc import Sequence, Callable
from .numerics import differentiate
from .auxfuncs import reduce_args


def newton_rhapson_solver(objective_value: float, func: Callable, initial_guess: float, args: Sequence=None, argument_index: int=None, max_steps: int=100, epsilon: float=0.0000001, differentiation_step=0.0000001, verbose_step=True, retry=True) -> float:
    '''
    Newton Rhapson Solver for any Python function that returns a float number.
    ----------
    Parameters
    ----
        objective_value (float): Solution value to be achieved.
        func (Callable): Python objective function to be solved.
        initial_guess (float): Initial guess of the solution.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
        max_steps (int): Optional. Maximum number of iterations. Default is 100.
        epsilon (float): Optional. Stoping criteria: abs(step) < epsilon. Default is 0.0000001.
        differentiation_step (float): Optional. Step size for the differentiation. Default is 0.0000001.
        verbose_step (bool): Optional. If True, prints the current step. Default is True.
        retry (bool): Optional. If True, retries the algorithm if the initial guess is not a solution. Default is True.
    ----
    Returns
    ----
        solution (float): Estimated solution value.
    '''
    func = reduce_args(func, args, argument_index)

    step = 1_000.0 * epsilon
    solution = initial_guess
    steps = 0
    try:
        while abs(step) > epsilon or steps > max_steps:
            estimated_value = func(solution)
            slope = differentiate(func, solution, argument_index)
            step = (estimated_value - objective_value) / slope
            solution -= step
            steps += 1
        if abs(step) > epsilon:
            raise ValueError(f'Maximum number of steps reached, but convergence criteria not met. Last step: {step} > epsilon: {epsilon}.')
        return solution
        
    except ZeroDivisionError as zde:
        if verbose_step:
            print('ZeroDivisionError: slope is zero')
        if retry:
            if verbose_step:
                print('Retrying...')
            solution = newton_rhapson_solver(objective_value, func, initial_guess, args, argument_index, max_steps, epsilon * 10, differentiation_step * 10, verbose_step, retry=False)
            return solution
        else:
            raise zde

def bisection_solver(objective_value: float, func: Callable, lower_bound: float, higher_bound: float, args: Sequence=None, argument_index: int=None, epsilon: float=0.0000001, max_iters: int=100) -> float:
    '''
    Bisection Solver for any Python function that returns a float number.
    ----------
    Parameters
    ----
        objective_value (float): Solution value to be achieved.
        func (Callable): Python objective function to be solved.
        lower_bound (float): Lower bound guess of the solution.
        higher_bound (float): Higher bound guess of the solution.
        args (Sequence): Optional. Sequence of arguments to be passed to the function. Example: func(x, y) -> z, args = [x, y]. Not needed if function has only one parameter (default None)
        arg_index (int): Optional. Index of the argument to be passed to the function. Example: func(x, y) -> z, arg_index = 1. Not needed if function has only one parameter (default None)
        epsilon (float): Optional. Stoping criteria: abs(step) < epsilon. Default is 0.0000001.
        max_iters (int): Optional. Maximum number of iterations. Default is 100.    
    ----
    Returns
    ----
        solution (float): Estimated solution value.
    '''
    func = reduce_args(func, args, argument_index)
    def objective_function(x):
        return func(x) - objective_value
    
    guess = (lower_bound + higher_bound) / 2.0
    iters = 0
    while iters < max_iters:
        f_guess = objective_function(guess)
        f_lower_bound = objective_function(lower_bound)
        aux = f_guess * f_lower_bound
        if abs(aux) < epsilon:
            return guess
        iters += 1
        if aux > 0:
            lower_bound = guess
        elif aux < 0:
            higher_bound = guess
        guess = (lower_bound + higher_bound) / 2.0

    if abs(aux) > epsilon:
        raise ValueError(f'Maximum number of iterations reached, but convergence criteria not met. f_low*f_guess: {aux} > epsilon: {epsilon}.')
    
    return guess