import abc
import functools

from typing import Callable

__all__ = ["CacheEngine", "key_fn", "memoize"]


class CacheEngine(metaclass=abc.ABCMeta):
    """
    Interface used to define Cache backends
    """

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value, expiry):
        pass


class MemcachedEngine(CacheEngine):
    def __init__(self, host: str = "localhost", port: int = 11211):
        from pymemcache.client import base
        self._client = base.Client((host, port))

    def get(self, key):
        return self._client.get(key)

    def set(self, key, value, expiry):
        self._client.set(key, value, expiry)


class RedisEngine(CacheEngine):
    def __init__(self, host: str = "localhost", port: int = 6379):
        import redis
        self._client = redis.Redis(host=host, port=port)

    def get(self, key):
        return self._client.get(key)

    def set(self, key, value, expiry):
        self._client.set(key, value, ex=expiry, )


class InMemoryEngine(CacheEngine):
    """
    >>> engine = InMemoryEngine(2)
    >>> engine.set("a", 1)
    >>> engine.set("b", 2)
    >>> engine.get("b")
    2
    >>> engine.get("a")
    1
    >>> engine.get("c")
    """

    def __init__(self, limit: int, expiration: int = 0):
        from lru import LRUCacheDict
        self._client = LRUCacheDict(max_size=limit, expiration=expiration)

    def get(self, key):
        try:
            return self._client[key]
        except KeyError:
            return None

    def set(self, key, value, expiry=None):
        if expiry:
            raise ValueError(
                f"Expiration should not be defined while setting single value using {self.__class__}, "
                f"Please pass expiration parameter in the object creation")
        self._client[key] = value


class FileEngine(CacheEngine):
    # TODO implement
    def __init__(self):
        import diskcache as dc

    def get(self, key):
        return None

    def set(self, key, value, expiry):
        return None


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
    >>> @memoize(InMemoryEngine, expiry=10):
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
