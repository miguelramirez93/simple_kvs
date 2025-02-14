import json
from threading import Lock
from typing import Any

from collection.errors import (
    CreateCollectionError,
    CreateError,
    DeleteError,
    GetError,
    KeyNotFoundError,
    SetError,
)
from collection.item import Item, Metadata
from shared.date.clock import ClockReader, DateTimeReader
from shared.encode.json import JsonEncoder
from storage.errors import DataNotFoundError
from storage.storage import Storage


class ReadWriter:
    _storage_client: Storage
    _clock_reader: ClockReader = DateTimeReader()
    _locker: Lock = Lock()

    def __init__(
        self,
        storage_cli_impl: Storage,
        clock_reader_impl: ClockReader | None = None,
    ) -> None:
        self._storage_client = storage_cli_impl
        if clock_reader_impl is not None:
            self._clock_reader = clock_reader_impl

    def create_collection(self, collection_name: str) -> None:
        with self._locker:
            try:
                self._storage_client.create_container(collection_name)
            except Exception as e:
                raise CreateCollectionError(e)

    def set(self, collection: str, key: str, value: Any):
        with self._locker:
            try:
                stored_item = self.get(collection, key)
                if stored_item is None:
                    self._create_item(collection, key, value)
                    return
                self._update_item(collection, key, stored_item, value)

            except Exception as e:
                raise SetError(e)

    def _create_item(self, collection: str, key: str, value: Any):
        try:
            now = self._clock_reader.now()
            item = Item(key, value, Metadata(now.strftime(
                "%m/%d/%Y, %H:%M:%S"), now.strftime("%m/%d/%Y, %H:%M:%S"), 1))
            item_bytes = JsonEncoder.encode(item.__dict__)
            self._storage_client.write(collection, key, item_bytes)
        except Exception as e:
            raise CreateError(e)

    def _update_item(self, collection: str, key: str, old_item: Item, value: Any):
        try:
            now = self._clock_reader.now()
            old_item.meta.version += 1
            old_item.meta.last_update_at = now.strftime("%m/%d/%Y, %H:%M:%S")
            old_item.value = value
            item_bytes = JsonEncoder.encode(old_item.__dict__)
            self._storage_client.write(collection, key, item_bytes)
        except Exception as e:
            raise CreateError(e)

    def get(self, collection: str, key: str) -> Item | None:
        try:
            item_bytes = self._storage_client.get(collection, key)
            item_json_str = item_bytes.decode()
            item_dict = json.loads(item_json_str)
            item_dict["meta"] = Metadata(**item_dict["meta"])
            return Item(**item_dict)
        except DataNotFoundError:
            return None
        except Exception as e:
            raise GetError(e)

    def delete(self, collection: str, key: str):
        with self._locker:
            try:
                self._storage_client.delete(collection, key)
            except DataNotFoundError:
                raise KeyNotFoundError(key)
            except Exception as e:
                raise DeleteError(e)
