from typing import Union, Annotated, Optional
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from starlette import status
from models import *


class Api:
    def __init__(self, config) -> None:
        self.config = config
        self.tts = None
        self.tgcalls = None
        self.app = FastAPI()
    
        @self.app.post("/call")
        async def call(call_request: CallRequest):
            return "Not implemented"
        
        @self.app.get("/health", dependencies=[Depends(self.auth)])
        @self.app.get("/")
        async def health_check():
            return {"health": "OK"}

    def run(self):    
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'])

    async def auth(self, auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        auth_token = self.config['api.auth_token']
        if auth_token and auth_token != auth.credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token missing or unknown")