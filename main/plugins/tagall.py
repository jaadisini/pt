import asyncio
import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from main.helpers.utils.handler import BOT

# daftar chat yang sedang berjalan tag
__MODULE__ = "Tagall"
__DESCRIPTION__ = "<blockquote>#Tagall</blockquote>"
__COMMANDS__ = """
⦿ /all : `Untuk Mention semua member`
⦿ /cancel : 'Untuk Menghentikan Mention'
"""
tagallgcid = []


DURASI_BTN = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⏱ 1 Menit", callback_data="tagdurasi_1"),
            InlineKeyboardButton("⏱ 3 Menit", callback_data="tagdurasi_3"),
            InlineKeyboardButton("⏱ 5 Menit", callback_data="tagdurasi_5"),
        ],
        [
            InlineKeyboardButton("⏱ 10 Menit", callback_data="tagdurasi_10"),
            InlineKeyboardButton("⏱ 15 Menit", callback_data="tagdurasi_15"),
        ],
        [
            InlineKeyboardButton("⏱ 20 Menit", callback_data="tagdurasi_20"),
            InlineKeyboardButton("⏱ 30 Menit", callback_data="tagdurasi_30"),
        ],
        [InlineKeyboardButton("❌ Batal", callback_data="tagdurasi_cancel")],
    ]
)


@BOT.COMMAND("all|tagall", filters.group)
@BOT.ADMIN
async def tagall_command(client, message):
    chat_id = message.chat.id

    if chat_id in tagallgcid:
        return await message.reply_text(
            "⚠️ Proses tag sudah berjalan di grup ini.\nGunakan /cancel untuk menghentikan."
        )

    text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Tagging semua member!"

    # kirim tombol durasi sebelum mulai
    await message.reply_text(
        f"⏳ Silakan pilih durasi berhenti otomatis untuk tagall :\n\n"
        f"<blockquote>{text}</blockquote>",
        reply_markup=DURASI_BTN,
    )


@BOT.CALLBACK("tagdurasi_(.*)")
async def _(client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id

    # hanya admin/owner yang diproses, user biasa diabaikan
    member = await client.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        return

    if data == "cancel":
        return await callback_query.message.edit_text("❌ Tagall dibatalkan sebelum dimulai.")

    try:
        menit = int(data)
    except Exception:
        return

    if chat_id in tagallgcid:
        return

    tagallgcid.append(chat_id)

    # hapus tombol setelah dipilih
    await callback_query.message.edit_text(f"✅ Tagall dimulai. Akan otomatis berhenti dalam {menit} menit.")

    # ambil pesan /all yang asli
    message = callback_query.message.reply_to_message or callback_query.message

    asyncio.create_task(stop_tagall_timer(chat_id, menit, callback_query.message))
    await mulai_tagall(client, message, chat_id)


async def mulai_tagall(client, message, chat_id):
    text = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else "Tagging semua member!"
    users = []

    async for member in client.get_chat_members(chat_id):
        if not (member.user.is_bot or member.user.is_deleted):
            if chat_id not in tagallgcid:  # cancel manual/otomatis
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

    # bersihkan dari daftar aktif jika selesai natural
    try:
        tagallgcid.remove(chat_id)
    except Exception:
        pass


async def stop_tagall_timer(chat_id, menit, msg):
    await asyncio.sleep(menit * 60)
    if chat_id in tagallgcid:
        tagallgcid.remove(chat_id)
        try:
            await msg.reply_text(f"⏱ Waktu {menit} menit habis, tagall dihentikan otomatis.")
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
