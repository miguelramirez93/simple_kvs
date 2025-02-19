from fastapi import APIRouter, Response, status

from collection.item import Item
from server.rest.deps import app_deps
from server.rest.routes.errors import UnexpectedHTTPException
from server.rest.routes.models import AddItemRequest

router = APIRouter()


@router.post("/v1/collections/{collection_name}", status_code=status.HTTP_201_CREATED)
def add_collection(collection_name: str):
    try:
        app_deps.collection_read_writer.create_collection(collection_name)
    except Exception as e:
        raise UnexpectedHTTPException(e)


@router.post("/v1/collections/{collection_name}/items/{key}/set", status_code=status.HTTP_201_CREATED)
def add_item(collection_name: str, key: str, request: AddItemRequest):
    try:
        app_deps.collection_read_writer.set(
            collection_name, key, request.__dict__)
    except Exception as e:
        raise UnexpectedHTTPException(e)


@router.get("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_200_OK)
def get_item(collection_name: str, key: str, response: Response) -> Item | None:
    try:
        item = app_deps.collection_read_writer.get(collection_name, key)
        if item is None:
            response.status_code = status.HTTP_404_NOT_FOUND
        return item
    except Exception as e:
        raise UnexpectedHTTPException(e)


@router.delete("/v1/collections/{collection_name}/items/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(collection_name: str, key: str):
    try:
        app_deps.collection_read_writer.delete(collection_name, key)
    except Exception as e:
        raise UnexpectedHTTPException(e)
