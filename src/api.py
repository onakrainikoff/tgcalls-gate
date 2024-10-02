from typing import Union
from fastapi import FastAPI
import uvicorn

class Api:
    def __init__(self) -> None:
        self.config = None
        self.tts = None
        self.tgcalls = None
        
        # !todo configuration
        self.app = FastAPI()

        @self.app.post("/call")
        async def call():
            return "Not implemented"
        
        @self.app.get("/health")
        @self.app.get("/")
        async def health_check():
            return {"health": "OK"}

    def run(self):    
        uvicorn.run(self.app, host="0.0.0.0", port=80)