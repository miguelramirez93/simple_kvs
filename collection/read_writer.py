from typing import Any
from collection.errors import SetError
from collection.item import Item
from storage.storage import Storage


class ReadWriter:
    _storage_client: Storage

    def __init__(self, storage_cli_impl: Storage) -> None:
        self._storage_client = storage_cli_impl

    def set(self, collection: str, key: str, value: Any):
        try:
            self._storage_client.write(collection, key, value)
        except Exception as e:
            raise SetError(e=e)

    def get(self, collection: str, key: str) -> Item:
        raise NotImplementedError

    def delete(self, collection: str, key: str):
        self._storage_client.delete(collection, key)
