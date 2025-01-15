import abc


class Storage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def write(self, container: str, key: str, data: bytes) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, container: str, key: str) -> bytes:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, container: str, key: str) -> None:
        raise NotImplementedError
