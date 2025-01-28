from fastapi import FastAPI, HTTPException, Response, status
from collection.item import Item
from storage.storage_files import FilesStorage
from collection.read_writer import ReadWriter
from typing import Any
from pydantic import BaseModel

app = FastAPI()


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
        raise HTTPException(
            status_code=500,
            detail=f"unexpected error happens: {e}"
        )


@app.post("/v1/collections/{collection_name}/items", status_code=status.HTTP_201_CREATED)
def add_item(collection_name: str, request: AddItemRequest):
    try:
        itemsReadWriter.set(collection_name, request.key, request.value)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"unexpected error happens: {e}"
        )


@app.get("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_200_OK)
def get_item(collection_name: str, key: str, response: Response) -> Item | None:
    try:
        item = itemsReadWriter.get(collection_name, key)
        if item is None:
            response.status_code = status.HTTP_404_NOT_FOUND
        return item
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"unexpected error happens: {e}"
        )


@app.delete("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(collection_name: str, key: str):
    try:
        itemsReadWriter.delete(collection_name, key)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"unexpected error happens: {e}"
        )
