import asyncio
import random
from pyrogram import filters
from pyrogram.errors import FloodWait
from main.helpers.utils.handler import BOT

# daftar chat yang sedang berjalan tag
tagallgcid = []


@BOT.COMMAND("all|tagall", filters.group)
@BOT.ADMIN
async def tagall_command(client, message):
    chat_id = message.chat.id

    if chat_id in tagallgcid:
        return await message.reply_text("⚠️ Proses tag sudah berjalan di grup ini.\nGunakan /cancel untuk menghentikan.")

    tagallgcid.append(chat_id)

    text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Tagging semua member!"
    users = []

    async for member in client.get_chat_members(chat_id):
        if not (member.user.is_bot or member.user.is_deleted):
            if chat_id not in tagallgcid:  # cancel manual
                break

            targetnya = f"• <a href=tg://user?id={member.user.id}>{member.user.first_name} {member.user.last_name or ''}</a>"
            users.append(targetnya)

            if len(users) == 5:
                random.shuffle(users)
                anu = "\n".join(users)
                try:
                    await asyncio.sleep(2)
                    await message.reply_text(
                        f"<blockquote>{text}</blockquote>\n"
                        f"<blockquote><b>{anu}</b></blockquote>\n"
                        f"<b><blockquote>🛒 @NakamaMarket</blockquote></b>",
                        quote=False,
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await asyncio.sleep(2)
                    await message.reply_text(
                        f"<blockquote>{text}</blockquote>\n"
                        f"<blockquote><b>{anu}</b></blockquote>\n"
                        f"<b><blockquote>🛒 @NakamaMarket</blockquote></b>",
                        quote=False,
                    )
                users = []

    # sisa user < 5
    if users and chat_id in tagallgcid:
        random.shuffle(users)
        anu = "\n".join(users)
        try:
            await asyncio.sleep(2)
            await message.reply_text(
                f"<blockquote>{text}</blockquote>\n"
                f"<blockquote><b>{anu}</b></blockquote>\n"
                f"<b><blockquote>🛒 @NakamaMarket</blockquote></b>",
                quote=False,
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await asyncio.sleep(2)
            await message.reply_text(
                f"<blockquote>{text}</blockquote>\n"
                f"<blockquote><b>{anu}</b></blockquote>\n"
                f"<b><blockquote>🛒 @NakamaMarket</blockquote></b>",
                quote=False,
            )

    # bersihkan dari daftar aktif
    try:
        tagallgcid.remove(chat_id)
    except Exception:
        pass


@BOT.COMMAND("cancel", filters.group)
@BOT.ADMIN
async def cancel_tag(client, message):
    chat_id = message.chat.id
    if chat_id in tagallgcid:
        tagallgcid.remove(chat_id)
        await message.reply_text("✅ Proses tag dihentikan.")
    else:
        await message.reply_text("⚠️ Tidak ada proses tag yang sedang berjalan.")
