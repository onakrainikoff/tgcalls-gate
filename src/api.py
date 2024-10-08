import logging, uvicorn, datetime
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

        @self.app.post("/call/{chat_id}", dependencies=[Depends(self.auth)])
        async def call(chat_id:int, content: CallContent) -> CallEntity:
            log.info(f"Request /call: chat_id={chat_id}, content={content}")
            entity = CallEntity(chat_id=chat_id, content=content)
            if content.text_to_speech:
                try:
                    self.tts_service.process(entity.id, content.text_to_speech)
                except Exception as ex:
                    entity.status = Status.ERROR
                    entity.status_details = f"PocessTextToSpeechError: chat_id={entity.chat_id}, id={entity.id}, error={type(ex)}:{ex} "
            elif not content.audio_url:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either 'audio_url' or 'text_to_speech' must be present")
            await self.tgcalls_service.process_call(entity)
            log.info(f"Response: chat_id={chat_id}, id={entity.id}, status={entity.status}, status_details={entity.status_details}")
            return entity 
         
        @self.app.post("/message/{chat_id}", dependencies=[Depends(self.auth)])
        async def message(chat_id:int, content: MessageContent) -> MessageEntity:
            log.info(f"Request /message: chat_id={chat_id}, content={content}")
            entity = MessageEntity(chat_id=chat_id, content=content)
            await self.tgcalls_service.process_message(entity)
            log.info(f"Response: chat_id={chat_id}, id={entity.id}, status={entity.status}, status_details={entity.status_details}")
            return entity
            
        
        @self.app.post("/call/test/{chat_id}", dependencies=[Depends(self.auth)])
        async def call_test(chat_id:int) -> CallEntity:
            log.info(f"Request /call/test/: chat_id={chat_id}")
            entity = await self.tgcalls_service.make_test_call(chat_id)
            log.info(f"Response: chat_id={chat_id}, id={entity.id}, status={entity.status}, status_details={entity.status_details}")
            return entity
        
        @self.app.get("/")
        @self.app.get("/health")
        async def health_check() -> dict:
            return {"health": "OK"}
        

    async def auth(self, auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
        auth_token = self.config['api.auth_token']
        if auth_token and (not auth or not auth.credentials or auth_token != auth.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token missing or unknown")
    
    
    def run(self):
        log.info("Starting TgCalls-Gate.API")
        uvicorn.run(self.app, host=self.config['api.host'], port=self.config['api.port'], log_config=None if self.config.get('logging') else uvicorn.config.LOGGING_CONFIG)
