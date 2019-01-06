import datetime
from contextlib import contextmanager

__all__ = ["log_perf_ctx", "log_perf"]


def _log_perf(start, end, msg):
    """
    Simple log function, log to stdout ( used by the ctx manager and the decorator)
    :param start: start time
    :param end: end time
    :param msg: log message
    :return:
    """
    print(f"[{start-end}] {msg}")


@contextmanager
def log_perf_ctx(msg, log_fn=_log_perf):
    """
    Log Performance context manager, log the performance at the __exit__

    Basic Usage:
    >>> with log_perf_ctx("finished execution"):
    ...     task()

    :param msg: log message
    :param log_fn: log function
    :return:
    """
    start = datetime.datetime.now()
    yield
    end = datetime.datetime.now()
    log_fn(start, end, msg)


def log_perf(msg=""):
    """
    Log Performance function decorator, produces a side effect as a log containing the perf log

    Basic Usage:
    >>> @log_perf("finish!")
    ... def tst():
    ...     pass

    :param msg: the log message
    :return:
    """

    def wrapped(f):
        def wrapper(*args, **kwargs):
            with log_perf_ctx('[{}] {}'.format(f.__name__, msg)):
                return f(*args, **kwargs)

        return wrapper

    return wrapped
