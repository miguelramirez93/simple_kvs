from typing import Any
import json
from collection.errors import DeleteError, GetError, SetError
from collection.item import Item
from storage.storage import Storage


class ReadWriter:
    _storage_client: Storage

    def __init__(self, storage_cli_impl: Storage) -> None:
        self._storage_client = storage_cli_impl

    def set(self, collection: str, key: str, value: Any):
        try:
            self._storage_client.write(collection, key, bytes(value))
        except Exception as e:
            raise SetError(e=e)

    def get(self, collection: str, key: str) -> Item:
        try:
            item_bytes = self._storage_client.get(collection, key)
            item_json_str = item_bytes.decode()
            item: Item = json.loads(item_json_str)
            return item
        except Exception as e:
            raise GetError(e)

    def delete(self, collection: str, key: str):
        try:
            self._storage_client.delete(collection, key)
        except Exception as e:
            raise DeleteError(e)
