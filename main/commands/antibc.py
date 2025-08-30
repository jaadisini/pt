from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.database import groupdb

__MODULE__ = "Protect"
__DESCRIPTION__ = "<blockquote>#Protect</blockquote>"
__COMMANDS__ = """
⦿ /protect on/off: `Untuk MengAktifkan Protect Atau Mematikan Protect`
"""

async def antibc_func(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title
    
    command = command_parser(message)
    
    if command == "on":
        success_text = f"Ptotect is enabled for {chat_title}"
        failed_text = f"Protect is already enabled for {chat_title}"
        runantibc = await groupdb.add_group(chat_id, True)
        if runantibc:
            await notification(message, success_text)
        else:
            await notification(message, failed_text)
    elif command == "off":
        success_text = f"Protect is disabled for {chat_title}"
        failed_text = f"Protect is already disabled for {chat_title}"
        runantibc = await groupdb.add_group(chat_id, False)
        if runantibc:
            await notification(message, success_text)
        else:
            await notification(message, failed_text)
    else:
        await notification(message, "Invalid command. Use '/protect on' to enable or '/protect off' to disable.")
