import datetime
from dataclasses import dataclass
from typing import Any


@dataclass
class Metadata:
    created_at: datetime.datetime
    last_update_at: datetime.datetime
    version: int


@dataclass
class Item:
    key: str
    value: Any
    meta: Metadata
