from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from pytgcalls import PyTgCalls, compose, idle
from pytgcalls.types import MediaStream, Update
import logging, asyncio, os
from asyncio import Event
from envyaml import EnvYAML
from .models import *

log = logging.getLogger()

class TgCallsSevice:
    def __init__(self, config:EnvYAML) -> None:
        log.info("Initialize TgCallsSevice")
        self.config = config
        self.tgcalls_dir = os.path.join(config['data_dir'], 'tgcalls')
        os.makedirs(self.tgcalls_dir, exist_ok=True)
        self.tg_client = Client (
            config['tgcalls.client.name'],
            api_id=config['tgcalls.client.api_id'],
            api_hash=config['tgcalls.client.api_hash'],
            phone_number=config['tgcalls.client.phone_number'],
            workdir=self.tgcalls_dir, 
        )
        self.tg_calls_client = PyTgCalls(self.tg_client)
        @self.tg_client.on_message()
        async def on_message(_: Client, message: Message):
            log.info(f"on_message: {message}")

    async def process(self, call:Call) -> None:
        event = asyncio.Event()
        chat_id = call.call_request.chat_id
        if call.call_request.message_before:
            await self.tg_client.send_message(chat_id, "call.call_request.message_before")
        func = self.tg_calls_client.add_handler(self._create_handler_for(chat_id, event))
        try:
            await self.tg_calls_client.play(
                chat_id,
                MediaStream(
                    call.audio_file,
                    video_flags=MediaStream.Flags.IGNORE,
                ),
            )
        except Exception as ex :
            print(ex)
            self.tg_calls_client.remove_handler(func)
            return
        
        await event.wait()
        self.tg_calls_client.remove_handler(func)
        await self.tg_calls_client.leave_call(chat_id)

        if call.call_request.send_audio_after_call:
            await self.tg_client.send_message(chat_id, "call.call_request.send_audio_after_call")

        if call.call_request.message_after:
            await self.tg_client.send_message(chat_id, "call.call_request.message_after")    
    
    def _create_handler_for(self, chat_id: int, event:Event):
        async def _updates(tg_call_client: PyTgCalls, update: Update):
            if update.chat_id == chat_id:
                event.set()
        return _updates