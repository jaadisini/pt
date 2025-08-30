from pyrogram import filters
from main.helpers.utils.handler import BOT
from main.commands import *

"""
antibc.py
"""
@BOT.COMMAND("protect")
@BOT.ADMIN
async def _(client, message):
    await antibc_func(client, message)

"""
whitelist.py
"""
@BOT.COMMAND("approve")
@BOT.ADMIN
async def _(client, message):
    await add_whitelist_func(client, message)

@BOT.COMMAND("unapprove")
@BOT.ADMIN
async def _(client, message):
    await remove_whitelist_func(client, message)

@BOT.COMMAND("listapprove")
@BOT.ADMIN
async def _(client, message):
    await list_whitelist_func(client, message)

"""
blockword.py
"""
@BOT.COMMAND("bl")
@BOT.ADMIN
async def _(client, message):
    await add_blockword(client, message)

@BOT.COMMAND("delbl")
@BOT.ADMIN
async def _(client, message):
    await remove_blockword(client, message)

@BOT.COMMAND("getbl")
@BOT.ADMIN
async def _(client, message):
    await list_blockwords(client, message)

@BOT.COMMAND("checkword")
@BOT.ADMIN
async def _(client, message):
    await check_blockword(client, message)

"""
message.py
"""
@BOT.ONMESSAGE(filters.group & filters.incoming)
@BOT.NONADMIN
async def _(client, message):
    await message_func(client, message)


