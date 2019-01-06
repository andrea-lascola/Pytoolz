from typing import Callable, List

__all__ = ["compose", "pipe"]


def compose(f1: Callable, f2: Callable) -> Callable:
    """
    Compose two functions: return the fn composition of the two

    Basic Usage:
    >>> f = compose(lambda x: x * 2,
    ...             lambda x: x * 3)
    >>> f(10)
    60

    :param f1: function 1
    :param f2: function 2
    :return:
    """
    return lambda x: f1(f2(x))


def pipe(functions: List[Callable], obj):
    """
    Recursively apply a list of morphism to an input value

    Basic Usage:
    >>> pipe([lambda x: x * 3,
    ...       lambda x: x * 2,
    ...       lambda x: x / 3], 10)
    20.0

    :param functions: list of functions
    :param obj: value
    :return: transformed value
    """
    if not functions:
        return obj

    return pipe(functions[1:], functions[0](obj))
