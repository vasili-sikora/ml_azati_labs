import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    res = []
    for k, v in dct.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            res.extend(traverse_dictionary_immutable(v, full_key))
        else:
            res.append((full_key, v))

    return res

def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for k, v in dct.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            traverse_dictionary_mutable(v, result, full_key)
        else:
           result.append((full_key, v))


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    res = []
    stack = list(reversed(list(dct.items())))

    while stack:
        full_key, value = stack.pop()

        if isinstance(value, dict):
            for k,v in reversed(list(value.items())):
                stack.append((f"{full_key}.{k}", v))
        else:
            res.append((full_key, value))

    return res
