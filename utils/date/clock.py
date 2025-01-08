import abc
import datetime


class ClockReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def now(self) -> datetime.datetime:
        raise NotImplementedError


class DateTimeReader(ClockReader):
    def __init__(self) -> None:
        super().__init__()

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()
