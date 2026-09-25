def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    return [x**2 for x in elements]


# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    return [i + 1 for i in range(len(elements))]


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """

    if not elements:
        return None
    return max(range(len(elements)), key=lambda i: elements[i])


# ====================================================================================================
def max[ObjT, KeyT](arr: Iterable[ObjT], key: Callable[[ObjT], KeyT]):
    it = iter(arr)
    max = next(it)
    for i in it:
        if key(i) > key(max):
            max = i

    return max


def eq[ObjT](arr: Iterable[ObjT], cmp: Callable[[ObjT, Obj], bool]):
    # < true
    # >= false
    res = cmp(a, b)
    res1 = cmp(b, a)
    if not res and not res1:
        return "Не равно"


def foo(a, b, cmp):
    # < -1
    # == 0
    # > 1
    if cmp(a, b) == True:
        return -1
    if cmp(b, a) == False:
        return 0
    return 1


def cmp(a, b, key):
    # key - ср. балл
    # return ср балл a < ср балл b
    return key(a) < key(b)


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    if len(elements) < 2:
        return []
    return elements[1::2]


# ====================================================================================================


def get_first_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    if not elements:
        return None
    for i, x in enumerate(elements):
        if x == 3:
            return i
    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> int | None:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    if not elements:
        return None
    for i, x in enumerate(reversed(elements)):
        if x == 3:
            return len(elements) - 1 - i
    return None


# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(
    elements: list[int], default: int | None
) -> tuple[int | None, int | None]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    if not elements:
        return default, default
    return min(elements), max(elements)


# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> int | None:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    if (value := elements[i]) > boundary:
        return value
    return None
