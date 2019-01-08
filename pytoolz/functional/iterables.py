from decimal import Decimal
from functools import reduce, partial
from typing import Callable, Iterable, List

from pytoolz.functional.pipe import compose

__all__ = ["flat_map", "iflat_map", "for_each", "Stream"]


def flat_map(fn: Callable, collection: Iterable):
    """
    Apply the input function to every element in iterable and flatten the result list
    :param fn: map function
    :param collection: input iterable
    :return: flattened collection

    >>> flat_map(lambda x: [x, x],[1,2,3])
    [1, 1, 2, 2, 3, 3]
    >>> flat_map(lambda x: (x, x),[1,2,3])
    [1, 1, 2, 2, 3, 3]
    """

    return reduce(lambda acc, x: acc + [y for y in x], map(fn, collection), [])


def iflat_map(fn: Callable, collection: Iterable):
    """
    Apply the input function to every element in iterable and flatten the result list lazily
    :param fn: map function
    :param collection: input iterable
    :return: flattened collection

    >>> list(iflat_map(lambda x: [x, x],[1,2,3]))
    [1, 1, 2, 2, 3, 3]
    >>> list(iflat_map(lambda x: (x, x),[1,2,3]))
    [1, 1, 2, 2, 3, 3]
    """
    for result in map(fn, collection):
        for element in result:
            yield element


def for_each(fn: Callable, collection: Iterable):
    """
    Create side effect applying the input function for every element in iterable
    :param fn: map function
    :param collection: input iterable
    :return: flattened collection

    >>> for_each(lambda x: print(x),[1,2,3])
    1
    2
    3
    """
    for x in collection:
        fn(x)


class Stream:
    """
    Basic Usage:
    >>> Stream([1,2,3]).map(lambda x: x*3).to_list()
    [3, 6, 9]
    >>> Stream([1,2,3]).sum().to_int()
    6
    >>> Stream([1,2,3]).map(lambda x: x*3).filter(lambda x: x >= 6).to_tuple()
    (6, 9)
    >>> Stream(["a","b","c"]).map(lambda x: x+"a").to_set() == {'aa', 'ba', 'ca'}
    True
    >>> Stream(["a","b","c"]).map(lambda x: x+"a").take(2).to_set() == {'aa', 'ba'}
    True
    >>> Stream([1, 4, 3])\
        .map(lambda x: x + 3)\
        .map(lambda x: x * x)\
        .filter(lambda x: x > 3)\
        .sum()\
        .to_float()
    101.0

    Alternative constructor
    >>> Stream.of([1,2,3], [
    ... (Stream.map, lambda x: x*3),
    ... (Stream.map, lambda x: x*3)
    ... ]).to_list()
    [9, 18, 27]
    """

    def __init__(self, iterable: Iterable):
        self._iterable: Iterable = iterable
        self.processor: Callable = lambda x: x

    @classmethod
    def of(cls, iterable: Iterable, functions: Iterable):
        instance = cls(iterable)
        for processor, fn in functions:
            processor(instance, fn)
        return instance

    def _collect(self, fn: Callable):
        obj = fn(self.processor(self._iterable))
        return obj

    # Public APIs
    def map(self, fn: Callable) -> 'Stream':
        self.processor = compose(partial(map, fn), self.processor)
        return self

    def flat_map(self, fn: Callable) -> 'Stream':
        self.processor = compose(partial(iflat_map, fn), self.processor)
        return self

    def filter(self, fn: Callable) -> 'Stream':
        self.processor = compose(partial(filter, fn), self.processor)
        return self

    def reduce(self, fn: Callable) -> 'Stream':
        self.processor = compose(partial(reduce, fn), self.processor)
        return self

    def find_first(self, fn: Callable) -> 'Stream':
        self.processor = compose(partial(reduce, fn), self.processor)
        return self

    def for_each(self, fn: Callable) -> None:
        self.processor = compose(partial(for_each, fn), self.processor)

    def take(self, limit: int) -> 'Stream':
        def fn(collection):
            for index, element in enumerate(collection):
                if index >= limit:
                    break
                yield element

        self.processor = compose(fn, self.processor)
        return self

    # Collectors

    def sum(self) -> 'Stream':
        self.processor = compose(sum, self.processor)
        return self

    def to_list(self) -> List:
        return self._collect(list)

    def to_int(self) -> int:
        return self._collect(int)

    def to_float(self) -> float:
        return self._collect(float)

    def to_decimal(self) -> Decimal:
        return self._collect(Decimal)

    def to_string(self) -> str:
        return self._collect(str)

    def to_tuple(self) -> tuple:
        return self._collect(tuple)

    def to_set(self) -> set:
        return self._collect(set)

    def to(self, fn: Callable):
        return self._collect(fn)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
