from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from main.helpers.utils.handler import BOT
from main.database import groupdb
from main import bot
from config import CBOT, COWNER, DEV

TEXT_START = """Hai, [{}](tg://user?id={})

**Telah digunakan :** `{}` group

<blockquote>AntiGcast bot otomatis menghapus Gcast di grup kamu.</blockquote>
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
        markup = InlineKeyboardMarkup(buttons)
        text = (
            f"<a href=tg://user?id={message.from_user.id}>"
            f"{message.from_user.first_name} {message.from_user.last_name or ''}</a>\n\n"
            f"<code>{message.text}</code>"
        )

        await client.send_message(6305402536, text, reply_markup=markup)
        await client.send_message(DEV, text, reply_markup=markup)


@BOT.COMMAND("start", filters.private)
async def start_command(client, message):
    await send_msg_to_owner(client, message)

    user = message.from_user
    group_count = await groupdb.count_all_groups()
    text = TEXT_START.format(user.mention, user.id, group_count)

    # pastikan sudah ada bot.me.username (diinit saat start bot)
    username = (await bot.get_me()).username

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✚ Add To Your Group", url=f"https://t.me/{username}?startgroup=true")],
            [
                InlineKeyboardButton("Commands", callback_data="CB_HELP"),
                InlineKeyboardButton("Owner", url=f"https://t.me/{COWNER.OWNER_USERNAME}"),
                InlineKeyboardButton("Store", url=f"https://t.me/NakamaMarket"),
            ],
            [InlineKeyboardButton("Close", callback_data="CB_CLOSE")],
        ]
    )

    return await message.reply_photo(
        photo=CBOT.BANNER_IMG_URL,
        caption=text,
        reply_markup=keyboard,
    )
