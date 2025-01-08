import abc
from typing import Any


class Storage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def Write(self, container: str, key: str, data: Any):
        raise NotImplementedError
