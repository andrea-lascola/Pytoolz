import abc
import pickle

try:
    import simplejson as json  # faster
except ImportError:
    import json

__all__ = ["BaseSerializer", "Json", "Dict", "Pickle"]


class BaseSerializer:
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    @abc.abstractmethod
    def serialize(self):
        pass

    @abc.abstractmethod
    def deserialize(self):
        pass


class Json(BaseSerializer):
    """
    From * to JSON
    """

    def serialize(self):
        return json.dumps(self._data)

    def deserialize(self):
        return json.loads(self._data)


class Pickle(BaseSerializer):
    """
    From * to Pickle
    """

    def serialize(self):
        return pickle.dumps(self._data)

    def deserialize(self):
        return pickle.loads(str(self._data))


class Dict(BaseSerializer):
    """
    From * to Dict
    """

    def serialize(self):
        return self._data.__dict__

    def deserialize(self):
        raise NotImplementedError("")
