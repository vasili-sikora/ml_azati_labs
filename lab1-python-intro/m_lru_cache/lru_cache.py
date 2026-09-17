from collections.abc import Callable
from functools import wraps
from typing import Any, OrderedDict, TypeVar

Function = TypeVar("Function", bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """
    if max_size <= 0:
        raise ValueError("Максимальный размер не может быть меньше или равен 0")

    cache = OrderedDict()

    def decorator(func: Function) -> Function:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, kwargs)
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            if len(cache) > max_size:
                cache.popitem(last=False)
            return result

        return wrapper

    return decorator
