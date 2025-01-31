import datetime
from abc import ABCMeta, abstractmethod


class ClockReader(metaclass=ABCMeta):
    @abstractmethod
    def now(self) -> datetime.datetime:
        pass


class DateTimeReader(ClockReader):
    def __init__(self) -> None:
        super().__init__()

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()
