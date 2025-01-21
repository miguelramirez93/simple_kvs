
class Storage():
    def write(self, container: str, key: str, data: bytes) -> None:
        raise NotImplementedError

    def get(self, container: str, key: str) -> bytes:
        raise NotImplementedError

    def delete(self, container: str, key: str) -> None:
        raise NotImplementedError
