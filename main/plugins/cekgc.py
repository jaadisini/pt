# plugins/check_group.py
from pyrogram import filters
from main.helpers.utils.handler import BOT
from main.database import groupdb
from config import CBOT


@BOT.COMMAND("cekgrup")
async def cek_grup(client, message):
    try:
        groups = await groupdb.get_all_groups()  # pastikan groupdb punya fungsi ini
        if not groups:
            return await message.reply_text("📭 Belum ada grup yang tersimpan di database.")

        text = "📋 <b>Daftar Grup Tersimpan</b>\n\n"
        for idx, group in enumerate(groups, start=1):
            chat_id = group.get("chat_id")
            state = "✅ Aktif" if group.get("state") else "❌ Nonaktif"
            text += f"{idx}. <code>{chat_id}</code> - {state}\n"

        # kalau list panjang, kirim ke log grup biar gak spam chat user
        if len(text) > 4000:
            await client.send_message(CBOT.LOG_GROUP_ID, text)
            await message.reply_text("📤 Daftar grup terlalu panjang, sudah dikirim ke log grup.")
        else:
            await message.reply_text(text)

    except Exception as e:
        await message.reply_text(f"⚠️ Gagal cek grup: {e}")
