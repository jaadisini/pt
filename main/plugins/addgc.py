# plugins/auto_add_group.py
from pyrogram import filters
from main.helpers.utils.handler import BOT
from main.database import groupdb
from config import LOG_GROUP_ID   # ganti owner dengan log group


@BOT.ONMESSAGE(filters.new_chat_members)
async def auto_add_group(client, message):
    for member in message.new_chat_members:
        if member.id == client.me.id:
            # simpan grup baru
            await groupdb.add_group(message.chat.id, state=False)

            # kirim konfirmasi ke grup
            await message.reply_text("✅ Bot berhasil ditambahkan dan grup tersimpan ke database.")

            # notifikasi ke log group
            try:
                chat = message.chat
                chat_title = chat.title or "Tanpa Nama"
                chat_id = chat.id
                inviter = message.from_user.mention if message.from_user else "Tidak diketahui"

                text = (
                    f"📥 <b>Bot ditambahkan ke grup baru!</b>\n\n"
                    f"🏷 Nama Grup: <code>{chat_title}</code>\n"
                    f"🆔 Chat ID: <code>{chat_id}</code>\n"
                    f"👤 Ditambahkan oleh: {inviter}"
                )
                await client.send_message(LOG_GROUP_ID, text)
            except Exception as e:
                print(f"Gagal kirim notifikasi log group: {e}")
