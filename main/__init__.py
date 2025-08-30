from pyrogram import Client
from pyrogram.handlers import CallbackQueryHandler, MessageHandler
from pyrogram.errors import FloodWait

from main.helpers.utils.logging import LOGGER

from config import CBOT

import sys
import asyncio

class BaseBot(Client):
    def __init__(self, **kwargs):
        super().__init__(
            name="BearBot",
            api_id=CBOT.API_ID,
            api_hash=CBOT.API_HASH,
            bot_token=CBOT.BOT_TOKEN,
            **kwargs,
        )

class Bot(BaseBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_message(self, filters=None, group=-1):
        def decorator(function):
            self.add_handler(MessageHandler(function, filters), group)
            return function
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(function):
            self.add_handler(CallbackQueryHandler(function, filters), group)
            return function
        return decorator

    async def start(self):
        try:
            await super().start()
            self.id = self.me.id
            self.username = self.me.username
            self.mention = self.me.mention
            LOGGER("init").info(f"» Importing Plugins for {self.username} ..")
        except FloodWait as e:
            await self.handle_flood_wait(e.value)
            await self.start()

    async def handle_flood_wait(self, wait_time):
        LOGGER("init").info(f"» FloodWait {wait_time} seconds ..")
        for remaining in range(wait_time, 0, -1):
            sys.stdout.write(f"\rWaiting {remaining} seconds.")
            sys.stdout.flush()
            await asyncio.sleep(1)

bot = Bot()