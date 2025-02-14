from abc import ABCMeta, abstractmethod


class Locker(metaclass=ABCMeta):
    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def release(self):
        pass
