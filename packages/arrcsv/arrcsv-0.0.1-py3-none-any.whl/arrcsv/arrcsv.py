import numpy as np

def convert_array(arr):
    """
    Convert an array to a string of comma-separated values.
    """
    return ','.join(map(str, arr))

def convert_2d_array_to_csv(arr):
    """
    Convert a 2D array to a string of comma-separated values.
    """
    return '\n'.join(map(convert_array, arr))

def convert_3d_array_to_csv(arr):
    """
    Convert a 3D array to a string of comma-separated values.
    """
    return '\n'.join(map(convert_2d_array_to_csv, arr))

def arr_to_csv(arr):
    """
    Convert an array to a string of comma-separated values.
    """
    array = np.array(arr)
    if len(array.shape) == 1:
        return convert_array(arr)
    elif len(array.shape) == 2:
        return convert_2d_array_to_csv(arr)
    elif len(array.shape) == 3:
        return convert_3d_array_to_csv(arr)
    else:
        raise ValueError('Array must be 1D, 2D, or 3D.')
    