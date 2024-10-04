import logging, sys, uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from envyaml import EnvYAML
from .models import *
from .tts import TtsService

log = logging.getLogger()

class Api:
    def __init__(self, config:EnvYAML, tts_service:TtsService ) -> None:
        log.info(f"Initialize Api")
        self.config = config
        self.tts_service = tts_service
        self.tgcalls = None
        self.app = FastAPI(title="TgCalls-Gate.Api")
    
        @self.app.post("/call", dependencies=[Depends(self.auth)])
        async def call(call_request: CallRequest):
            log.info(f"Received call_request: {call_request}")
            call = Call(call_request=call_request)
            if call_request.audio_url:
                call.audio_file = call_request.audio_url    
            elif call_request.text_to_speech:
                call.audio_file = self.tts_service.process(call.id, call_request.text_to_speech)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either 'audio_url' or 'text_to_speech' must be present")
            return call 
        
        @self.app.get("/health")
        @self.app.get("/")
        async def health_check():
            return {"health": "OK"}

    async def auth(self, auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        auth_token = self.config['api.auth_token']
        if auth_token and (not auth or not auth.credentials or auth_token != auth.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token missing or unknown")
    
    def run(self):
        log.info("Starting TgCalls-Gate.API")
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'], log_config=None if self.config.get('logging') else uvicorn.config.LOGGING_CONFIG)
