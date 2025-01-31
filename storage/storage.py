from abc import ABCMeta, abstractmethod


class Storage(metaclass=ABCMeta):

    @abstractmethod
    def create_container(self, container: str) -> None:
        pass

    @abstractmethod
    def write(self, container: str, key: str, data: bytes) -> None:
        pass

    @abstractmethod
    def get(self, container: str, key: str) -> bytes:
        pass

    @abstractmethod
    def delete(self, container: str, key: str) -> None:
        pass
