import numpy as np
import numpy.typing as npt


def replace_nans(matrix: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    res = matrix.copy()
    # [1, nan, 3]
    nan_msk = np.isnan(res)
    # [True, False, True]
    if nan_msk.all():
        return np.zeros_like(res)

    avg = np.nanmean(res)
    res[nan_msk] = avg
    return res


def __pls__(self, obj) -> np.Array:
    res = np.zeros_like(obj)
    for i in range(len(obj)):
        res[i] = self[i] + obj[i]


def __eq__(self, obj) -> bool:
    res = np.zeros_like(obj)
    for i in range(len(obj)):
        res[i] = self[i] == obj[i]

[1, nan, 3]
np.isnan()
[False, True, False]