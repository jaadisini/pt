import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

from main.database.matadb import *
from main.helpers.utils.handler import BOT


@BOT.ONMESSAGE(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=3,
)
async def cek_mataa(client: Client, message: Message):
    # Skip jika message dari channel / sangmata mati
    if message.sender_chat or not message.from_user:
        return

    if not await is_sangmata_on(message.chat.id):
        return

    user = message.from_user
    user_id = user.id

    # Jika belum ada di database → langsung simpan
    if not await cek_userdata(user_id):
        await add_userdata(user_id, user.username, user.first_name, user.last_name)
        return

    username_before, first_before, last_before = await get_userdata(user_id)

    changes = []

    # Cek perubahan username
    if username_before != user.username:
        old = f"@{username_before}" if username_before else "Tanpa Username"
        new = f"@{user.username}" if user.username else "Tanpa Username"
        changes.append(f"• Username berubah dari <b>{old}</b> ke <b>{new}</b>")

    # Cek perubahan nama depan
    if first_before != user.first_name:
        old = first_before or "Tanpa Nama"
        new = user.first_name or "Tanpa Nama"
        changes.append(f"• Nama depan berubah dari <b>{old}</b> ke <b>{new}</b>")

    # Cek perubahan nama belakang
    if last_before != user.last_name:
        old = last_before or "Tanpa Nama Belakang"
        new = user.last_name or "Tanpa Nama Belakang"
        changes.append(f"• Nama belakang berubah dari <b>{old}</b> ke <b>{new}</b>")

    # Jika ada perubahan → kirim log & update database
    if changes:
        text = (
            "👀 <b>Alea Sangmata</b>\n\n"
            f"User: {user.mention} [<code>{user_id}</code>]\n\n"
            + "\n".join(changes)
        )

        await message.reply_text(text, quote=True)

        # Update database sekali saja
        await add_userdata(user_id, user.username, user.first_name, user.last_name)


@BOT.COMMAND("sangmata", filters.group)
@BOT.ADMIN
async def set_mataa(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Gunakan:\n"
            "<code>/sangmata on</code> untuk mengaktifkan\n"
            "<code>/sangmata off</code> untuk menonaktifkan"
        )

    cmd = message.command[1].lower()

    if cmd == "on":
        if await is_sangmata_on(message.chat.id):
            return await message.reply_text("✅ Sangmata sudah aktif di grup ini.")
        
        await sangmata_on(message.chat.id)
        await message.reply_text("✅ Sangmata berhasil diaktifkan.")

    elif cmd == "off":
        if not await is_sangmata_on(message.chat.id):
            return await message.reply_text("❌ Sangmata sudah nonaktif.")
        
        await sangmata_off(message.chat.id)
        await message.reply_text("❌ Sangmata berhasil dinonaktifkan.")

    else:
        await message.reply_text("Parameter tidak valid. Gunakan hanya: on / off.")
