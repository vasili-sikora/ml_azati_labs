import inspect
from collections import OrderedDict
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

Function = TypeVar("Function", bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """
    def decorator(func: Function) -> Callable[..., Any]:
        cache_dict: OrderedDict[tuple, Any] = OrderedDict()
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            key = tuple(bound_args.arguments.items())

            if key in cache_dict:
                cache_dict.move_to_end(key)
                return cache_dict[key]
            result = func(*args, **kwargs)
            cache_dict[key] = result

            if len(cache_dict) > max_size:
                cache_dict.popitem(last=False)

            return result
        return wrapper
    return decorator
