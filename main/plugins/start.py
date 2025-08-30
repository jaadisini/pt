from pyrogram import filters
from pykeyboard import InlineButton, InlineKeyboard
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton

from main.helpers.utils.handler import BOT
from main.database import groupdb
from main import bot
from config import CBOT,COWNER
from config import DEV

TEXT_START = """Hey yooo, [{}](tg://user?id={})

**Telah digunakan oleh :** `{}` group

<blockquote> I am an AntiGcast bot whose job is to automatically delete Gcast in your group.</blockquote>
"""

async def send_msg_to_owner(client, message):
    if message.from_user.id == 6305402536:
        return
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    "👤 ᴘʀᴏꜰɪʟ", callback_data=f"profil {message.from_user.id}"
                ),
                InlineKeyboardButton(
                    "ᴊᴀᴡᴀʙ 💬", callback_data=f"jawab_pesan {message.from_user.id}"
                ),
            ],
        ]
        await client.send_message(
            6305402536,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
	await client.send_message(
            DEV,
            f"<a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n<code>{message.text}</code>",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@BOT.COMMAND("start", filters.private)
async def start_command(client, message):
    await send_msg_to_owner(client, message)
    user = message.from_user
    group_count = await groupdb.count_all_groups()
    text = TEXT_START.format(user.mention, user.id, group_count)
    keyboard = InlineKeyboard()
    keyboard.row(InlineButton("✚ Add To Your Grup", url=f"https://t.me/{bot.me.username}?startgroup=true"))
    keyboard.row(
        InlineButton("Commands", "CB_HELP"),
        InlineButton("Owner", url=f"https://t.me/{COWNER.OWNER_USERNAME}"),
    )
    keyboard.row(InlineButton("Close", "CB_CLOSE"))

    return await message.reply_photo(
        photo=CBOT.BANNER_IMG_URL,
        caption=text,
        reply_markup=keyboard,
    )

