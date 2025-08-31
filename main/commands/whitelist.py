from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.database import userdb, groupdb

__MODULE__ = "Whitelist"
__DESCRIPTION__ = "<blockquote>#WhitelistUser</blockquote>"
__COMMANDS__ = """
⦿ /wl [user_id / reply]: `Menambahkan user agar pesan tidak dihapus.`
⦿ /delwl [user_id / reply]: `Menghapus dari daftar whitelist.`
⦿ /listwl : `Melihat daftar Whitelist.`
"""

__ISPRO__ = False

async def get_user_id_and_mention(client, message):
    user_id = None
    user_mention = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
    elif message.entities:
        for entity in message.entities:
            if entity.type == "text_mention":
                user_id = entity.user.id
                user_mention = entity.user.mention
                break
            elif entity.type == "mention":
                username = message.text[entity.offset:entity.offset+entity.length]
                try:
                    user = await client.get_users(username)
                    user_id = user.id
                    user_mention = user.mention
                except Exception:
                    pass
                break
    if not user_id and command_parser(message):
        try:
            user = await client.get_users(command_parser(message))
            user_id = user.id
            user_mention = user.mention
        except Exception:
            pass
    return user_id, user_mention

async def add_whitelist_func(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title

    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "Please mention a user, reply to their message, or provide a valid user ID.")
        return
    try:
        addwhiteuser = await userdb.add_to_whitelist(user_id)
        if addwhiteuser:
            await notification(message, f"Successfully added {user_mention} to {chat_title} whitelist")
        else:
            await notification(message, f"Failed to add {user_mention} to {chat_title} whitelist. They might already be in the whitelist.")
    except Exception as e:
        await notification(message, f"Error occurred: {str(e)}")

async def remove_whitelist_func(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title

    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "Please mention a user, reply to their message, or provide a valid user ID.")
        return
    try:
        removewhiteuser = await userdb.remove_from_whitelist(user_id)
        if removewhiteuser:
            await notification(message, f"Successfully removed {user_mention} from {chat_title} whitelist")
        else:
            await notification(message, f"Failed to remove {user_mention} from {chat_title} whitelist. They might not be in the whitelist.")
    except Exception as e:
        await notification(message, f"Error occurred: {str(e)}")

async def list_whitelist_func(client, message):
    chat_id = message.chat.id
    chat = await client.get_chat(chat_id)
    chat_title = chat.title

    whitelistusers = await userdb.get_whitelist(user_id)
    if whitelistusers:
        text = f"Whitelisted users in {chat_title}:\n"
        for user_id in whitelistusers:
            user = await client.get_users(user_id)
            text += f" {user.mention}\n"
        await message.reply(f"<blockquote>{text}</blockquote>")
    else:
        await notification(message, f"No whitelisted users in {chat_title}")
