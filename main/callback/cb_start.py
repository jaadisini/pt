from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pykeyboard import InlineButton, InlineKeyboard

from main import bot
from main.helpers.utils.handler import BOT
from main.database import groupdb
from config import COWNER

TEXT_START = """Hey yooo, [{}](tg://user?id={})

**Telah digunakan oleh :** `{}` group

<blockquote> I am an AntiGcast bot whose job is to automatically delete Gcast in your group.</blockquote>
"""

@BOT.CALLBACK("^CB_START")
async def _(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    user_mention = callback.from_user.mention
    group_count = await groupdb.count_all_groups()
    text = TEXT_START.format(user_mention, user_id, group_count)
    keyboard = InlineKeyboard()
    keyboard.row(InlineButton("✚ Ads To Your Group", url=f"https://t.me/{bot.me.username}?startgroup=true"))
    keyboard.row(
        InlineButton("Commands", "CB_HELP"),
        InlineButton("Owner", url=f"https://t.me/{COWNER.OWNER_USERNAME}"),
        InlineButton("Store", url=f"https://t.me/NakamaMarket"),
    )
    keyboard.row(InlineButton("Close", "CB_CLOSE"))
    return await callback.edit_message_text(text, reply_markup=keyboard)

CREATOR = [
    6305402536
]
SUPPORT = []

@BOT.CALLBACK("^jawab_pesan")
async def _(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await client.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.append(get.id)
    try:
        button = [
            [InlineKeyboardButton("❌ BATALKAN", callback_data=f"batal {user_id}")]
        ]
        pesan = await client.ask(
            user_id,
            f"<b>✉️ SILAHKAN KIRIM BALASAN ANDA: {full_name}</b>",
            reply_markup=InlineKeyboardMarkup(button),
            timeout=300,
        )
    except asyncio.TimeoutError:
        if get.id not in SUPPORT:
            return
        else:
            SUPPORT.remove(get.id)
            await pesan.delete()
            return await client.send_message(1623499141, "Pembatalan Otomatis")
    text = f"<b>✅ PESAN BALASAN ANDA TELAH TERKIRIM: {full_name}</b>"
    if user_ids not in [CREATOR]:
        buttons = [[InlineKeyboardButton("💬 Jawab Pesan 💬", f"jawab_pesan {user_id}")]]
    else:
        buttons = [
            [
                InlineKeyboardButton("👤 Profil", callback_data=f"profil {user_id}"),
                InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    if get.id not in SUPPORT:
        return
    else:
        try:
            await pesan.copy(
                user_ids,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            SUPPORT.remove(get.id)
            await client.edit_message_text(
                user_id,
                pesan.id - 1,
                f"<b>✉️ SILAHKAN KIRIM BALASAN ANDA: {full_name}</b>",
            )
            await callback_query.message.delete()
            return await client.send_message(user_id, text)
        except Exception as error:
            return await client.send_message(user_id, error)

@BOT.CALLBACK("^profil")
async def profil_callback(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split()[1])
    try:
        bot = await client.get_me()
        get = await client.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ɪᴅ ᴘᴇɴɢɢᴜɴᴀ:</b> <code>{get.id}</code>\n"
            f"<b> ┣ ɴᴀᴍᴀ ᴅᴇᴘᴀɴ:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ ɴᴀᴍᴀ ʙᴇʟᴀᴋᴀɴɢɴʏᴀ:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ ᴜsᴇʀɴᴀᴍᴇ:</b> @{username}\n"
        msg += f"<b> ┗ ʙᴏᴛ: {bot.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(why)
