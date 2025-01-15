import json
from typing import Any
from collection.errors import DeleteError, GetError, SetError
from collection.item import Item, Metadata
from shared.encode.json import JsonEncoder
from storage.storage import Storage
from shared.date.clock import ClockReader, DateTimeReader


class ReadWriter:
    _storage_client: Storage
    _clock_reader: ClockReader = DateTimeReader()

    def __init__(
        self,
        storage_cli_impl: Storage,
        clock_reader_impl: ClockReader | None = None,
    ) -> None:
        self._storage_client = storage_cli_impl
        if clock_reader_impl is not None:
            self._clock_reader = clock_reader_impl

    def set(self, collection: str, key: str, value: Any):
        try:
            now = self._clock_reader.now()
            item = Item(key, value, Metadata(now, now, 1))
            item_bytes = JsonEncoder.encode(item.__dict__)
            self._storage_client.write(collection, key, item_bytes)
        except Exception as e:
            raise SetError(e)

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
