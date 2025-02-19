from typing import Any

from pydantic import BaseModel


class AddItemRequest(BaseModel):
    value: Any
