import asyncio
from pyrogram import Client, enums
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
    keyboard.row(
        InlineKeyboardButton(
            "✚ Ads To Your Group", 
            url=f"https://t.me/{bot.me.username}?startgroup=true",
            style=enums.ButtonStyle.PRIMARY
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            "Commands", 
            callback_data="CB_HELP",
            style=enums.ButtonStyle.PRIMARY
        ),
        InlineKeyboardButton(
            "Channel", 
            url="https://t.me/NakamaHire",
            style=enums.ButtonStyle.PRIMARY
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            "Close", 
            callback_data="CB_CLOSE",
            style=enums.ButtonStyle.DANGER
        )
    )
    return await callback.edit_message_text(text, reply_markup=keyboard)

CREATOR = [
    1816904396
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
            [
                InlineKeyboardButton(
                    "❌ BATALKAN", 
                    callback_data=f"batal {user_id}",
                    style=enums.ButtonStyle.DANGER
                )
            ]
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
            return await client.send_message(1816904396, "Pembatalan Otomatis")
            
    text = f"<b>✅ PESAN BALASAN ANDA TELAH TERKIRIM: {full_name}</b>"
    if user_ids not in CREATOR:
        buttons = [
            [
                InlineKeyboardButton(
                    "💬 Jawab Pesan 💬", 
                    callback_data=f"jawab_pesan {user_id}",
                    style=enums.ButtonStyle.PRIMARY
                )
            ]
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 Profil", 
                    callback_data=f"profil {user_id}",
                    style=enums.ButtonStyle.PRIMARY
                ),
                InlineKeyboardButton(
                    "Jawab 💬", 
                    callback_data=f"jawab_pesan {user_id}",
                    style=enums.ButtonStyle.SUCCESS
                ),
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
            return await client.send_message(user_id, str(error))

@BOT.CALLBACK("^profil")
async def profil_callback(client: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split()[1])
    try:
        bot_user = await client.get_me()
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
        if last_name != "None" and get.last_name:
            msg += f"<b> ┣ ɴᴀᴍᴀ ʙᴇʟᴀᴋᴀɴɢɴʏᴀ:</b> {last_name}\n"
        if username != "None" and get.username:
            msg += f"<b> ┣ ᴜsᴇʀɴᴀᴍᴇ:</b> @{username}\n"
        msg += f"<b> ┗ ʙᴏᴛ: {bot_user.mention}\n"
        
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                    style=enums.ButtonStyle.PRIMARY
                )
            ]
        ]
        await callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(str(why))
