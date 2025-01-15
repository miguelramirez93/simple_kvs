import json
from typing import Any


class JsonEncoder:
    @staticmethod
    def encode(target: dict[str, Any]) -> bytes:
        str_dict = json.dumps(target)
        return str_dict.encode()
