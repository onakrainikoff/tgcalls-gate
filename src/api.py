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
        async def call(chat_id:int, call_request: CallRequest) -> CallResponse:
            call_request.created_at = datetime.now()
            call_request.id = get_id()
            log.info(f"Request /call: chat_id={chat_id}, call_request={call_request}")
            call_response = CallResponse(chat_id=chat_id, call_request=call_request)
            if call_request.text_to_speech:
                self.tts_service.process(call_request.id, call_request.text_to_speech)
            elif not call_request.audio_url:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Either 'audio_url' or 'text_to_speech' must be present")
            await self.tgcalls_service.process_call(call_response)
            log.info(f"CallResponse: chat_id={chat_id}, id={call_response.call_request.id}, status={call_response.status}, status_details={call_response.status_details}")
            return call_response 
         
        @self.app.post("/message/{chat_id}", dependencies=[Depends(self.auth)])
        async def mwssage(chat_id:int, message_request: MessageRequest) -> MessageResponse:
            message_request.created_at = datetime.now()
            message_request.id = get_id()
            log.info(f"Request /message: chat_id={chat_id}, message_request={message_request}")
            message_response = MessageResponse(chat_id=chat_id, message_request=message_request)
            await self.tgcalls_service.process_message(message_response)
            log.info(f"MessageResponse: chat_id={chat_id}, id={message_response.message_request.id}, status={message_response.status}, status_details={message_response.status_details}")
            return message_response
            
        
        @self.app.post("/call/test/{chat_id}", dependencies=[Depends(self.auth)])
        async def call_test(chat_id:int) -> CallResponse:
            log.info(f"Request /call/test/: chat_id={chat_id}")
            call_response = await self.tgcalls_service.make_test_call(chat_id)
            log.info(f"CallResponse: chat_id={chat_id}, id={call_response.call_request.id}, status={call_response.status}, status_details={call_response.status_details}")
            return call_response
        
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
