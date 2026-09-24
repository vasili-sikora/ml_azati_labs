import numpy as np
import numpy.typing as npt


def add_zeros(x: npt.NDArray[np.int_]) -> npt.NDArray[np.int_]:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    if len(x) <= 1:
        return x

    x = np.insert(x, np.arange(1, len(x)), 0)
    return x
