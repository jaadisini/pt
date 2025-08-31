from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.helpers.utils.handler import BOT
from main.database import userdb  # instance dari UsersDB


# ===== Ambil user ID + mention =====
async def get_user_id_and_mention(client, message):
    user_id = None
    user_mention = None

    # Prioritas: reply dulu
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention

    # Kalau ada entity (mention / text_mention)
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

    # Kalau ada argumen setelah command
    if not user_id:
        arg = command_parser(message)
        if arg:
            if arg.isdigit():  # langsung kasih user_id
                user_id = int(arg)
                try:
                    user = await client.get_users(user_id)
                    user_mention = user.mention
                except Exception:
                    user_mention = f"<code>{user_id}</code>"
            else:  # mungkin username
                try:
                    user = await client.get_users(arg)
                    user_id = user.id
                    user_mention = user.mention
                except Exception:
                    pass

    return user_id, user_mention


# ===== Add Global Blacklist =====
@BOT.COMMAND("dor")
@BOT.OWNER
async def add_global_blacklist(client, message):
    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "⚠️ Harap reply, mention, username, atau beri user ID.")
        return

    already_blacklisted = await userdb.is_blacklisted(user_id)
    if already_blacklisted:
        await notification(message, f"{user_mention} sudah ada di blacklist global.")
        return

    await userdb.add_to_blacklist(user_id)
    await notification(message, f"✅ {user_mention} berhasil ditambahkan ke blacklist global.")


# ===== Remove Global Blacklist =====
@BOT.COMMAND("undor")
@BOT.OWNER
async def remove_global_blacklist(client, message):
    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "⚠️ Harap reply, mention, username, atau beri user ID.")
        return

    already_blacklisted = await userdb.is_blacklisted(user_id)
    if not already_blacklisted:
        await notification(message, f"{user_mention} tidak ada di blacklist global.")
        return

    await userdb.remove_from_blacklist(user_id)
    await notification(message, f"✅ {user_mention} berhasil dihapus dari blacklist global.")


# ===== List Global Blacklist =====
@BOT.COMMAND("listdor")
@BOT.OWNER
async def list_global_blacklist(client, message):
    blacklist = await userdb.get_blacklist()

    if not blacklist:
        await notification(message, "⚠️ Tidak ada user dalam blacklist global.")
        return

    text = "🚫 Global Blacklisted Users:\n"
    for uid in blacklist:
        try:
            user = await client.get_users(int(uid))
            text += f" - {user.mention}\n"
        except Exception:
            text += f" - <code>{uid}</code>\n"

    await message.reply(f"<blockquote>{text}</blockquote>")
