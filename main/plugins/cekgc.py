# plugins/check_group.py
from pyrogram import filters
from main.helpers.utils.handler import BOT
from main.database import groupdb
from config import LOG_GROUP_ID


@BOT.COMMAND("cekgrup")
async def cek_grup(client, message):
    try:
        groups = await groupdb.get_all_groups()  # return list of int
        if not groups:
            return await message.reply_text("📭 Belum ada grup yang tersimpan di database.")

        text = "📋 <b>Daftar Grup Tersimpan</b>\n\n"
        for idx, chat_id in enumerate(groups, start=1):
            text += f"{idx}. <code>{chat_id}</code>\n"

        if len(text) > 4000:
            await client.send_message(LOG_GROUP_ID, text)
            await message.reply_text("📤 Daftar grup terlalu panjang, sudah dikirim ke log grup.")
        else:
            await message.reply_text(text)

    except Exception as e:
        await message.reply_text(f"⚠️ Gagal cek grup: {e}")
