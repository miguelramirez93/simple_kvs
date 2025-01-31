from typing import Any

from fastapi import Response, status
from pydantic import BaseModel

from collection.item import Item
from collection.read_writer import ReadWriter
from server.rest.errors import UnexpectedHTTPException
from server.rest.middlewares import app
from storage.storage_files import FilesStorage

storage = FilesStorage()
itemsReadWriter = ReadWriter(storage)


class AddItemRequest(BaseModel):
    key: str
    value: Any


@app.post("/v1/collections/{collection_name}", status_code=status.HTTP_201_CREATED)
def add_collection(collection_name: str):
    try:
        itemsReadWriter.create_collection(collection_name)
    except Exception as e:
        raise UnexpectedHTTPException(e)


@app.post("/v1/collections/{collection_name}/items", status_code=status.HTTP_201_CREATED)
def add_item(collection_name: str, request: AddItemRequest):
    try:
        itemsReadWriter.set(collection_name, request.key, request.value)
    except Exception as e:
        raise UnexpectedHTTPException(e)


@app.get("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_200_OK)
def get_item(collection_name: str, key: str, response: Response) -> Item | None:
    try:
        item = itemsReadWriter.get(collection_name, key)
        if item is None:
            response.status_code = status.HTTP_404_NOT_FOUND
        return item
    except Exception as e:
        raise UnexpectedHTTPException(e)


@app.delete("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(collection_name: str, key: str):
    try:
        itemsReadWriter.delete(collection_name, key)
    except Exception as e:
        raise UnexpectedHTTPException(e)
