import logging, sys, uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from envyaml import EnvYAML
from models import *

log = logging.getLogger()

class Api:
    def __init__(self, config:EnvYAML) -> None:
        self.config = config
        self.tts = None
        self.tgcalls = None
        self.app = FastAPI(title="TgCalls-Gate.API")
    
        @self.app.post("/call", dependencies=[Depends(self.auth)])
        async def call(call_request: CallRequest):
            log.info(f"Received call_request: {call_request}")
            return Call(call_request=call_request)
        
        @self.app.get("/health")
        @self.app.get("/")
        async def health_check():
            return {"health": "OK"}

    async def auth(self, auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        auth_token = self.config['api.auth_token']
        if auth_token and auth_token != auth.credentials:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token missing or unknown")
    
    def run(self):
        log.info("Starting TgCalls-Gate.API")
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'], log_config=None if self.config.get('logging') else uvicorn.config.LOGGING_CONFIG)
