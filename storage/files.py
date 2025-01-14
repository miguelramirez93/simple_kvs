import os
from storage.errors import ContainerNotFoundError
from storage.storage import Storage


class FilesStorage(Storage):
    _data_path: str

    def __init__(self, data_path="./data") -> None:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        self._data_path = data_path

    def write(self, container: str, key: str, data: bytes):
        container_path = self._get_container_path(container)
        if not os.path.exists(container_path):
            os.makedirs(container_path)

        with open(f"{container_path}/{key}", "w+b") as key_file:
            key_file.write(data)

    def get(self, container: str, key: str) -> bytes:
        container_path = self._get_container_path(container)

        if not os.path.exists(container_path):
            raise ContainerNotFoundError(container)

        key_path = f"{container_path}/{key}"

        with open(key_path, "rb") as key_file:
            return key_file.read()

    def _get_container_path(self, container: str) -> str:
        return f"{self._data_path}/{container}"
