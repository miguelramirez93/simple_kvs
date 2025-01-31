import datetime
from dataclasses import dataclass
from typing import Any


@dataclass
class Metadata:
    created_at: str
    last_update_at: str
    version: int


@dataclass
class Item:
    key: str
    value: Any
    meta: Metadata
