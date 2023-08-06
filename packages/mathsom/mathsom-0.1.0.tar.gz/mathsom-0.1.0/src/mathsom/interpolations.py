from typing import Union, get_args
import numpy as np
from scipy.interpolate import CubicSpline
from collections.abc import Sequence
from enum import Enum

class InterpolationMethod(Enum):
    LINEAR = 'linear'
    LOGLINEAR = 'loglinear'
    CUBIC_SPLINE = 'cubic_spline'

def adapt_interpolation_result(x: Union[float, Sequence, np.ndarray], result: Union[float, Sequence, np.ndarray]) -> Union[float, np.ndarray]:
    '''
    Adapts interpolation result to the input x. If input is Sequence, result will be adapted to np.ndarray, else result will be a float.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        result (Union[float, Sequence, np.ndarray]): Interpolated y(x) value(s).
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Adapted interpolation result.
    '''

    if isinstance(x, get_args(Union[Sequence, np.ndarray])):
        result = np.array(result)
    elif isinstance(result, np.ndarray):
        if len(result.shape)==0:
            return float(result)
        else:
            return float(result[0])
    elif isinstance(result, Sequence):
        return float(result[0])

    return result

def check_pairs_interpolation(x_input: Union[Sequence, np.ndarray], y_input: Union[Sequence, np.ndarray]) -> None:
    if len(x_input) != len(y_input):
        raise ValueError(f'x_input and y_input must have the same length. x_input: {len(x_input)}, y_input: {len(y_input)}')

def linear_interpolation(x: Union[float, Sequence, np.ndarray], known_xs: Union[Sequence, np.ndarray], known_ys: Union[Sequence, np.ndarray]) -> Union[float, np.ndarray]:
    '''
    Linear interpolation. Interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    result = np.interp(x, known_xs, known_ys)
    return result

def loglinear_interpolation(x, known_xs, known_ys):
    '''
    Log linear interpolation. Interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    log_known_ys = np.log(known_ys)
    log_y_result = linear_interpolation(x, known_xs, log_known_ys)
    result = np.exp(log_y_result)
    return result
def cubic_spline_interpolation(x, known_xs, known_ys):
    '''
    Cubic spline interpolation. interpolates y(x) for a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
    ----
    Returns:
    ----
        result (Union[float, np.ndarray]): Interpolated y(x) value(s).
    '''
    cs = CubicSpline(known_xs, known_ys)
    result = cs(x)
    return result

interpolation_methods_map = {
    InterpolationMethod.LINEAR: linear_interpolation, 
    InterpolationMethod.LOGLINEAR: loglinear_interpolation, 
    InterpolationMethod.CUBIC_SPLINE: cubic_spline_interpolation
}

def interpolate(x: Union[float, Sequence, np.ndarray], known_xs: Union[Sequence, np.ndarray], known_ys: Union[Sequence, np.ndarray], interpolation_method: InterpolationMethod=InterpolationMethod.LINEAR) -> Union[float, np.ndarray]:
    '''
    Interpolates y(x) in a given number of pairs (x, y) received in 2 Sequence or np.ndarray of same length.    
    ----------
    Parameters:
    ----
        x (Union[float, Sequence, np.ndarray]): Value(s) to be interpolated.
        known_xs (Union[Sequence, np.ndarray]): Sequence or np.ndarray of x values.
        known_ys (Union[Sequence, np.ndarray]): Sequence or np.ndarray of y values.
        interpolation_method (InterpolationMethod): Optional. Interpolation method. Default is linear interpolation.
    ----
    Returns:
    ----
        Union[float, np.ndarray]
            Interpolated y(x) value(s).
    '''
    check_pairs_interpolation(known_xs, known_ys)
    interpolation_func = interpolation_methods_map[interpolation_method]
    result = interpolation_func(x, known_xs, known_ys)
    result = adapt_interpolation_result(x, result)
    return result

