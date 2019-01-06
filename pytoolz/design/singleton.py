__all__ = ["singleton", ]


def singleton(class_):
    """
    A Simple singleton decorator for classes
    Basic Usage:
    >>> @singleton
    ... class MyClass:
    ...    pass
    >>> id(MyClass()) == id(MyClass())
    True

    :param class_: decorated class
    :return: singleton instance
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
