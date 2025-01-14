import json


class JsonEncoder:
    @staticmethod
    def encode(target: dict) -> bytes:
        str_dict = json.dumps(target)
        return str_dict.encode()
