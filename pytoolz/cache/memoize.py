import abc
import functools
from abc import ABCMeta
from typing import Callable


class CacheEngine(metaclass=ABCMeta):
    """
    Interface used to define Cache backends
    #TODO define different backends : Redis/MC/in memory..
    """

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value, expiry):
        pass


def key_fn(func, args, kwargs):
    """
    Compose cache key using function name and function input parameters
    :param func: function
    :param args: function args
    :param kwargs: function kwargs
    :return: cache key string
    """
    sep = "||"
    return f"{func.__name__}{sep}PARAMS{sep}{sep.join(args)}".replace(' ', '')


def memoize(cache: CacheEngine, key_func: Callable = key_fn, expiry: int = 10):
    """
    Cache Decorator used to store decorated function result.
    It produces side effect calling get/set method of the cache engine

    Basic Usage:
    >>> @memoize(RedisEngine,expiry=10):
    ... def square(number):
    ...     return number **2

    :param cache: cache engine : implementation of CacheEngine interface
    :param key_func: function used to calculate the cache key using input fn parameters
    :param expiry: expiry time in seconds
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            key = str(key_func(func, args, kwargs))
            entry = cache.get(key)

            if entry:
                return entry
            else:
                entry = func(*args, **kwargs)
                cache.set(key, entry, expiry=expiry)
                return entry

        return _inner

    return decorator
