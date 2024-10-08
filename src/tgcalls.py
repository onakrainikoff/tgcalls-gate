from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, Update
from pytgcalls.exceptions import CallDeclined, TimedOutAnswer, CallDiscarded
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


    async def process_call(self, entity:CallEntity) -> None:
        log.info(f"Process call: {entity}")
        event = asyncio.Event()
        chat_id = entity.chat_id
        content = entity.content
        audio_file = content.audio_url if content.audio_url else content.text_to_speech.audio_file_path
        if content.message_before:
            message_entity = MessageEntity(chat_id=chat_id, content=content.message_before)
            await self.process_message(message_entity)
            if message_entity.status == Status.ERROR:
                entity.status = Status.ERROR
                entity.status_details = message_entity.status_details
                return
        call_handler = self.tg_calls_client.add_handler(self._create_call_handler(chat_id, event))
        try:
            await self.tg_calls_client.play(chat_id, MediaStream(audio_file, video_flags=MediaStream.Flags.IGNORE))
            await event.wait()
        except (CallDeclined, TimedOutAnswer, CallDiscarded) as fail:
            message = f"PocessCallFail: chat_id={chat_id}, id={entity.id}, fail={type(fail)}:{fail} "
            log.info(message)
            entity.status = Status.FAILED
            entity.status_details = message
        except Exception as ex:
            message = f"PocessCallError: chat_id={chat_id}, id={entity.id}, error={type(ex)}:{ex} "
            log.error(message)
            entity.status = Status.ERROR
            entity.status_details = message
            return
        finally:
            self.tg_calls_client.remove_handler(call_handler)
            event.set()
            try:
                await self.tg_calls_client.leave_call(chat_id)
            except:
                pass
        if content.send_audio_after_call:
            # !todo audio_url?
            try:
                await self.tg_client.send_audio(chat_id, audio=audio_file, progress=self._create_send_audio_handler)
            except Exception as ex:
                message = f"PocessCallSendAudioError: chat_id={chat_id}, id={entity.id}, error={type(ex)}:{ex} "
                log.error(message)
                entity.status = Status.ERROR
                entity.status_details = message
                return
        if content.message_after:
            message_entity = MessageEntity(chat_id=chat_id, content=content.message_after)
            await self.process_message(message_entity)
            if message_entity.status == Status.ERROR:
                entity.status = Status.ERROR
                entity.status_details = message_entity.status_details
                return


    async def process_message(self, entity:MessageEntity) -> None:
        log.info(f"Process message: {entity}")
        chat_id = entity.chat_id
        content = entity.content
        try:
            await self.tg_client.send_message(chat_id, content.text)
            entity.status = Status.SUCCESS
        except Exception as ex:
            message = f"PocessMessageError: chat_id={chat_id}, id={entity.id}, error={type(ex)}:{ex} "
            log.error(message)
            entity.status = Status.ERROR
            entity.status_details = message

    
    async def make_test_call(self, chat_id:int) -> CallEntity:
        log.info(f"Create test call for chat_id={chat_id}")
        text_to_speech= TextToSpeech(text="Hello! It`s test call by TgCalls-Gate ", lang='en')
        content = CallContent(chat_id=chat_id, text_to_speech=text_to_speech)
        entity = CallEntity(content=content)
        self.tts_service.process(entity.id, text_to_speech)
        await self.process_call(entity)
        return entity
    

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
            if update.chat_id == chat_id and (not event.is_set):                
                event.set()
        return _on_update
    
    
    def _create_message_handler(self):
        async def _on_message(_, message: Message):
            if message.chat.type == ChatType.PRIVATE:
                chat_id = message.chat.id
                if message.text == '!test':
                    call_entity = await self.make_test_call(chat_id)
                    log.debug(f"Response: {call_entity}")
                elif message.text:
                    message_entity= MessageEntity(chat_id=chat_id, content=MessageContent(text=f"Welcome to chat_id={chat_id}. Send !test to creat test call"))
                    await self.process_message(message_entity)
                    log.debug(f"Response: {message_entity}")
        return _on_message
    
    
    def _create_send_audio_handler(self, chat_id:int):
        async def _on_sendong_audio(current, total):
            log.info(f"Sending audio after call for {chat_id}: progress={current * 100 / total:.1f}%")         
        return _on_sendong_audio
