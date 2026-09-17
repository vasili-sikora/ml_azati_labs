from collections.abc import Generator
from typing import Any


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    if not matrix:
        return []

    transposed = []

    for row in range(len(matrix[0])):
        tr_row = []
        for col in range(len(matrix)):
            tr_row.append(matrix[col][row])
        transposed.append(tr_row)

    return transposed

def uniq(sequence: list[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
    the same order without duplicates
    """
    seen = set()
    for el in sequence:
        if el not in seen:
            yield el
            seen.add(el)


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictionary
    """
    res = {}
    for dct in dicts:
        res.update(dct)
    return res

def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum(lhs[i] * rhs[i] for i in range(len(lhs)))



if __name__ == "__main__":
    test_mtr = [[1,2], [3,4],[5,6]]

    print(transpose(test_mtr))

    test_seq = [3, 1, 3, 2, 1 , 4]

    for el in uniq(test_seq):
        print(el)

    print(dict_merge({"a": 1, "b": 2}, {"a": 10, "c": 3}))
