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


# [1, 1, 1, 1]
# [1, 0, 1, 0, 1, 0, 1]


print(type(np.arange(1, 2)))

# [1, "str", obj]

a = np.array(
    [
        [
            1213,
        ],
        1,
        1.0,
    ],
    dtype=np.object_,
)
a[0].append(213)
print(a)

a = 1
b = 1

print(a is b)

c = 257
d = 257

print(c is d)
