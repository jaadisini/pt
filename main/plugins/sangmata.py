import asyncio
import random
from pyrogram import *
from pyrogram.errors import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *
from pyrogram import enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatPermissions
from pyrogram.errors import UserNotParticipant

from main.helpers.admin_check import admin_filter
from AmonMusic.utils.matadb import *
from main import Bot




@Bot.on_message(
    filters.group & ~filters.bot & ~filters.via_bot,
    group=3,
)
async def cek_mataa(self: Client, ctx: Message):
    if ctx.sender_chat or not await is_sangmata_on(ctx.chat.id):
        return
    if not await cek_userdata(ctx.from_user.id):
        return await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    usernamebefore, first_name, lastname_before = await get_userdata(ctx.from_user.id)
    msg = ""
    if usernamebefore != ctx.from_user.username or first_name != ctx.from_user.first_name or lastname_before != ctx.from_user.last_name:
        msg += f"👀 <b>Alea Sangmata</b>\n\n User: {ctx.from_user.mention} [<code>{ctx.from_user.id}</code>]\n"
    if usernamebefore != ctx.from_user.username:
        usernamebefore = f"<blockquote>@{usernamebefore}" if usernamebefore else "<code>Tanpa Username</code></blockquote>"
        usernameafter = f"<blockquote>@{ctx.from_user.username}" if ctx.from_user.username else "<code>Tanpa Username</code></blockquote>"
        msg += f"<blockquote>`Mengubah username dari {usernamebefore} ke {usernameafter}.`\n</blockquote>"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if first_name != ctx.from_user.first_name:
        msg += f"<blockquote>`Mengubah nama depan dari {first_name} ke {ctx.from_user.first_name}.`\n</blockquote>"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if lastname_before != ctx.from_user.last_name:
        lastname_before = lastname_before or "`Tanpa Nama Belakang`"
        lastname_after = ctx.from_user.last_name or "`Tanpa Nama Belakang`"
        msg += f"<blockquote>`Mengubah nama belakang dari {lastname_before} ke {lastname_after}.`\n</blockquote>"
        await add_userdata(ctx.from_user.id, ctx.from_user.username, ctx.from_user.first_name, ctx.from_user.last_name)
    if msg != "":
        await ctx.reply_text(msg, quote=True)

@app.on_message(filters.group & filters.command("sangmata") & admin_filter)
#@app.on_message(filters.group & filters.command("sangmata") & ~filters.bot & ~filters.via_bot)
async def set_mataa(self: Client, ctx: Message):
    if len(ctx.command) == 1:
        return await ctx.reply_text("Gunakan <code>/on</code>, untuk mengaktifkan sangmata. Jika Anda ingin menonaktifkan, Anda dapat menggunakan parameter off.")
    if ctx.command[1] == "on":
        cekset = await is_sangmata_on(ctx.chat.id)
        if cekset:
            await ctx.reply_text("SangMata telah diaktifkan di grup Anda.")
        else:
            await sangmata_on(ctx.chat.id)
            await ctx.reply_text("Sangmata diaktifkan di grup Anda.")
    elif ctx.command[1] == "off":
        cekset = await is_sangmata_on(ctx.chat.id)
        if not cekset:
            await ctx.reply_text("SangMata telah dinonaktifkan di grup Anda.")
        else:
            await sangmata_off(ctx.chat.id)
            await ctx.reply_text("Sangmata dinonaktifkan di grup Anda.")
    else:
        await ctx.reply_text("Parameter tidak diketahui, gunakan hanya parameter on/off.", del_in=6)
    
