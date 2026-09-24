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
    nan_msk = np.isnan(res)

    if nan_msk.all():
        return np.zeros_like(res)

    avg = np.nanmean(res)
    res[nan_msk] = avg
    return res
