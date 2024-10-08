from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, Update
from pytgcalls.exceptions import CallDeclined, TimedOutAnswer, CallDiscarded, NotInCallError
import logging, asyncio, os, datetime, traceback
from asyncio import Event
from envyaml import EnvYAML
from .tts import TtsService
from .models import *

log = logging.getLogger()

class TgCallsSevice:
    def __init__(self, config:EnvYAML, tts_service:TtsService) -> None:
        log.info("Initialize TgCallsSevice")
        self.config = config
        self.tgcalls_dir = os.path.join(config['data_dir'], 'tgcalls')
        os.makedirs(self.tgcalls_dir, exist_ok=True)
        self.tts_service = tts_service


    async def process_call(self, call_response:CallResponse) -> None:
        call_request = call_response.call_request
        log.info(f"Process call_request={call_request}")
        event = asyncio.Event()
        chat_id = call_request.chat_id
        try:
            if call_request.message_before:
                message_request = call_request.message_before
                message_request.chat_id = chat_id
                message_response = MessageResponse(message_request=message_request)
                await self.process_message(message_response)
        
            audio_file = call_request.audio_url if call_request.audio_url else call_request.text_to_speech.audio_file_path
            call_handler = self.tg_calls_client.add_handler(self._create_call_handler(chat_id, event))
            try:
                await self.tg_calls_client.play(chat_id, MediaStream(audio_file, video_flags=MediaStream.Flags.IGNORE))
                await event.wait()
                self.tg_calls_client.remove_handler(call_handler)
                await self.tg_calls_client.leave_call(chat_id)
            except Exception as ex:
                log.error(f"Processing error for call_request.id={call_request.id}:{type(ex)}={ex}")
                traceback.print_exception(ex)
                call_response.status = Status.ERROR
                message_response.status_details = f"{type(ex)}={ex}"
                # !todo check call decline
                self.tg_calls_client.remove_handler(call_handler)
            
            # if call_request.send_audio_after_call:
            #     # !todo logging?
            #     # !todo audio_url?
            #     await self.tg_client.send_audio(chat_id, audio=call_request.text_to_speech.audio_file_path, progress=self._create_send_audio_handler)

            if call_request.message_after:
                message_request = call_request.message_after
                message_request.chat_id = chat_id
                message_response = MessageResponse(message_request=message_request)
                await self.process_message(message_response)
        except Exception as ex:
            log.error(f"Processing error for call_request.id={call_request.id}:{type(ex)}={ex}")
            traceback.print_exception(ex)
            call_response.status = Status.ERROR
            message_response.status_details = f"{type(ex)}={ex}"


    async def process_message(self, message_response:MessageResponse) -> None:
        message_request=message_response.message_request
        log.info(f"Process message_request={message_request}")
        chat_id = message_request.chat_id
        try:
            await self.tg_client.send_message(chat_id, message_request.text)
            message_response.status = Status.SUCCESS
        except Exception as ex:
            log.error(f"Processing error for message_request.id={message_request.id}: {ex}")
            message_response.status = Status.ERROR
            message_response.status_details = str(ex)


    async def make_test_call(self, chat_id:int) -> CallResponse:
        log.info(f"Create test call for chat_id={chat_id}")
        text_to_speech= TextToSpeech(text="Hello! It`s test call by TgCalls-Gate ", lang='en')
        call_request = CallRequest(id=get_id(), chat_id=chat_id, text_to_speech=text_to_speech)
        call_response = CallResponse(call_request=call_request)
        self.tts_service.process(call_request.id, text_to_speech)
        await self.process_call(call_response)
        return call_response
    

    async def connect(self) -> None:
        log.info("Connecting to Telegramm")
        self.tg_client = Client (
            self.config['tgcalls.client.name'],
            api_id=self.config['tgcalls.client.api_id'],
            api_hash=self.config['tgcalls.client.api_hash'],
            phone_number=self.config['tgcalls.client.phone_number'],
            workdir=self.tgcalls_dir
        )
        self.tg_client.add_handler(MessageHandler(self._create_message_handler()))
        self.tg_calls_client = PyTgCalls(self.tg_client)
        await self.tg_calls_client.start()
        log.info("Connection to Telegram is successful")

    
    def _create_call_handler(self, chat_id: int, event:Event):
        async def _on_update(_, update: Update):
            log.info(f">>>> call_handler: {update}")
            if update.chat_id == chat_id:                
                # !todo check update type?
                # !todo check even?
                event.set()
        return _on_update
    
    
    def _create_message_handler(self):
        async def _on_message(_, message: Message):
            if message.chat.type == ChatType.PRIVATE:
                chat_id = message.chat.id
                if message.text == '!test':
                    call_response = await self.make_test_call(chat_id)
                    log.debug(f"CallResponse: {call_response}")
                elif message.text:
                    message_request = MessageRequest(chat_id=chat_id, text=f"Welcome to chat_id={chat_id}. Send !test to creat test call")
                    message_response= MessageResponse(message_request=message_request)
                    await self.process_message(message_response)
                    log.debug(f"MessageResponse: {message_response}")
        return _on_message
    
    
    def _create_send_audio_handler(self, chat_id:int):
        async def _on_sendong_audio(current, total):
            log.info(f"Sending audio after call for {chat_id}: progress={current * 100 / total:.1f}%")         
        return _on_sendong_audio
