import logging, uvicorn, asyncio
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from envyaml import EnvYAML
from contextlib import asynccontextmanager
from .models import *
from .tts import TtsService
from .tgcalls import TgCallsSevice
from pyrogram.handlers import MessageHandler
from pyrogram.methods.utilities.idle import idle

log = logging.getLogger()

class Api:
    def __init__(self, config:EnvYAML, tts_service:TtsService, tgcalls_service:TgCallsSevice) -> None:
        log.info(f"Initialize Api")
        self.config = config
        self.tts_service = tts_service
        self.tgcalls_service = tgcalls_service
        self.app = FastAPI(title="TgCalls-Gate.Api")
        
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self.tgcalls_service.connect()           
            yield
        self.app.router.lifespan_context = lifespan        

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
         
        @self.app.post("/call/test/{chat_id}", dependencies=[Depends(self.auth)])
        async def call_test(chat_id:int):
            return await self.tgcalls_service.call_test(chat_id)
        
        # !todo make send message method

        @self.app.get("/")
        @self.app.get("/health")
        async def health_check():
            return {"health": "OK"}

    async def auth(self, auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        auth_token = self.config['api.auth_token']
        if auth_token and (not auth or not auth.credentials or auth_token != auth.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token missing or unknown")
    
    def run(self):
        log.info("Starting TgCalls-Gate.API")
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'], log_config=None if self.config.get('logging') else uvicorn.config.LOGGING_CONFIG)
