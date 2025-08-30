from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.database import blockwordsdb, groupdb

__MODULE__ = "Blacklist"
__DESCRIPTION__ = "<blockquote>#BlacklistText</blockquote>"
__COMMANDS__ = """
⦿ /bl [text/reply]: `Menambahkan Kata terlarang ke Daftar Blacklist.`
⦿ /delbl [text/reply]: `Menghapus dari daftar kata blacklist.`
⦿ /getbl : `Melihat daftar Blacklist.`
"""
__ISPRO__ = True

async def add_blockword(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title
    
    word = command_parser(message)
    if not word:
        await notification(message, "Please provide a word to block.")
        return
    
    success = await blockwordsdb.add_blockword(chat_id, word)
    if success:
        await notification(message, f"<b>{word}</b> has been added to {chat_title} blocklist.")
    else:
        await notification(message, f"<b>{word}</b> is already in {chat_title} blocklist.")

async def remove_blockword(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title
    
    word = command_parser(message)
    if not word:
        await notification(message, "Please provide a word to unblock.")
        return
    
    success = await blockwordsdb.remove_blockword(chat_id, word)
    if success:
        await notification(message, f"<b>{word}</b> has been removed from {chat_title} blocklist.")
    else:
        await notification(message, f"<b>{word}</b> is not in the {chat_title} blocklist.")

async def list_blockwords(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title
    
    blockwords = await blockwordsdb.get_blockwords(chat_id)
    if blockwords:
        word_list = ", ".join(blockwords)
        await message.reply(word_list, f"Blocked words in this group:\n> {word_list}")
    else:
        await notification(message, f"There are no blocked words in {chat_title} group.")
    return

async def check_blockword(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title
    
    word = command_parser(message)
    if not word:
        await notification(message, "Please provide a word to unblock.")
        return
    
    is_blocked = await blockwordsdb.is_blocked(chat_id, word)
    if is_blocked:
        await notification(message, f"<b>{word}</b> is blocked in {chat_title} group.")
    else:
        await notification(message, f"<b>{word}</b> is not blocked in {chat_title} group.")
