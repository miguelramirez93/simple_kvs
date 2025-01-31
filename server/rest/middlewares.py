from fastapi import FastAPI, Request

from server.rest.errors import UnexpectedHTTPException

app = FastAPI()

# TODO: Make this middleware work


@app.middleware("http")
async def exception_uncaught_middleware_catcher(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        raise UnexpectedHTTPException(e)
