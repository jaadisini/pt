# plugins/auto_add_group.py
from pyrogram import filters
from main.helpers.utils.handler import BOT
from main.database import groupdb


@BOT.on_message(filters.new_chat_members)
async def auto_add_group(client, message):
    for member in message.new_chat_members:
        if member.id == client.me.id:
            await groupdb.add_group(message.chat.id, state=False)
            await message.reply_text("✅ Bot berhasil ditambahkan dan grup tersimpan ke database.")
