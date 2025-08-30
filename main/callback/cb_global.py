from pyrogram import Client
from pyrogram.types import CallbackQuery
from main.helpers.utils.handler import BOT

@BOT.CALLBACK("^CB_CLOSE")
async def _(client: Client, callback: CallbackQuery):
    return await callback.message.delete()