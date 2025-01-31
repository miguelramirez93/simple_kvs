from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class UnexpectedHTTPException(HTTPException):
    def __init__(self, e: Exception) -> None:
        super().__init__(HTTP_500_INTERNAL_SERVER_ERROR,
                         f"unexpected error happens: {e}")
