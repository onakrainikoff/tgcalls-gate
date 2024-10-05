from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram.handlers import MessageHandler
from pyrogram.handlers.handler import Handler
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, Update
import logging, asyncio, os
from asyncio import Event
from envyaml import EnvYAML
from .tts import TtsService
from .models import *

log = logging.getLogger()

class MyMessageHandler(Handler):
    def __init__(self):
        pass

    async def check(self, client: Client, update: filters.Update):
            print(f"on_message: {update}")
            log.info(f"on_message: {update}")
            return True

class TgCallsSevice:
    def __init__(self, config:EnvYAML, tts_service:TtsService) -> None:
        log.info("Initialize TgCallsSevice")
        self.config = config
        self.tgcalls_dir = os.path.join(config['data_dir'], 'tgcalls')
        os.makedirs(self.tgcalls_dir, exist_ok=True)
        self.tts_service = tts_service

    # !todo setting statuses
    async def process(self, call:Call) -> None:
        log.info(f"Process call={call}")
        event = asyncio.Event()
        chat_id = call.call_request.chat_id
        if call.call_request.message_before:
            await self.tg_client.send_message(chat_id, "call.call_request.message_before")
        func = self.tg_calls_client.add_handler(self._create_call_handler(chat_id, event))
        try:
            await self.tg_calls_client.play(
                chat_id,
                MediaStream(
                    call.audio_file,
                    video_flags=MediaStream.Flags.IGNORE,
                ),
            )
        except Exception as ex :
            log.error(ex)
            self.tg_calls_client.remove_handler(func)
            call.result = CallResult.ERROR
        
        await event.wait()
        self.tg_calls_client.remove_handler(func)
        await self.tg_calls_client.leave_call(chat_id)
        
        if call.call_request.send_audio_after_call:
            await self.tg_client.send_message(chat_id, "call.call_request.send_audio_after_call")

        if call.call_request.message_after:
            await self.tg_client.send_message(chat_id, "call.call_request.message_after")    
    
    async def call_test(self, chat_id:int):
        log.info(f"Create test call for chat_id={chat_id}")
        test_text_to_speech= TextToSpeech(text="Hello! It`s test call by TgCalls-Gate ", lang='en')
        test_call_request = CallRequest(chat_id=chat_id, text_to_speech=test_text_to_speech)
        test_call = Call(call_request=test_call_request)
        test_call.audio_file = self.tts_service.process(test_call.id, test_text_to_speech)
        await self.process(test_call)
        return test_call

    # !todo sending messages
    
    async def connect(self):
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

    def _create_call_handler(self, chat_id: int, event:Event):
        async def _updates(tg_call_client: PyTgCalls, update: Update):
            if update.chat_id == chat_id:
                event.set()
        return _updates
    
    def _create_message_handler(self):
        async def _on_message(_, message: Message):
            if message.chat.type == ChatType.PRIVATE:
                if message.text == '!test':
                    await self.call_test(message.chat.id)
                elif message.text:
                    await message.reply(f"Welcome to chat_id={message.chat.id}. Send !test to creat test call")
        return _on_message
         
