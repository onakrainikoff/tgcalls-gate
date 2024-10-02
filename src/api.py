from typing import Union
from fastapi import FastAPI

class Api:
    def __init__(self) -> None:
        self.app = FastAPI()
        @self.app.get("/")
        async def read_root():
            return {"Hello": "World"}

        @self.app.get("/items/{item_id}")
        async def read_item(item_id: int, q: Union[str, None] = None):
            return {"item_id": item_id, "q": q}