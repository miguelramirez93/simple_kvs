from fastapi import FastAPI, status

from server.rest.routes import collections

app = FastAPI()

app.include_router(collections.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "pong"}
