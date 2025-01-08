from typing import Any
from storages.storage import Storage


class ReadWriter:
    _storage_client: Storage

    def __init__(self, storage_cli_impl: Storage) -> None:
        self._storage_client = storage_cli_impl

    def Add(self, collection: str, key: str, value: Any):
        self._storage_client.Write(collection, key, value)
