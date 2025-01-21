import dataclasses
import json
from typing import Any


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class JsonEncoder:
    @staticmethod
    def encode(target: dict[str, Any]) -> bytes:
        str_dict = json.dumps(target, cls=EnhancedJSONEncoder)
        return str_dict.encode()
