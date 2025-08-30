import asyncio
from pyrogram.errors import FloodWait, Forbidden
from main.helpers.utils.handler import BOT
from main.database import groupdb


@BOT.COMMAND("gcast")
@BOT.OWNER
async def _(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❗ Gunakan:\n<code>/gcast pesan</code>")
    
    text = message.text.split(None, 1)[1]

    groups = await groupdb.get_all_groups()
    if not groups:
        return await message.reply_text("⚠️ Tidak ada grup dalam database.")

    done = 0
    failed = 0

    status = await message.reply_text(f"⏳ Broadcast ke <b>{len(groups)}</b> grup...")

    for chat_id in groups:
        try:
            # pastikan chat_id integer
            chat_id = int(chat_id)

            # cek antibc_state
            if await groupdb.get_antibc_state(chat_id):
                continue

            await client.send_message(chat_id, text)
            done += 1
            await asyncio.sleep(0.5)

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Forbidden:
            failed += 1
        except Exception:
            failed += 1

    await status.edit_text(
        f"✅ <b>Broadcast Grup selesai</b>\n\n"
        f"• Sukses: <code>{done}</code>\n"
        f"• Gagal: <code>{failed}</code>\n"
        f"• Total: <code>{len(groups)}</code>"
    )
