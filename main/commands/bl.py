import json
import os
from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.database import userdb, groupdb



__ISPRO__ = False


# ===== Utils Blacklist =====
def load_blacklist():
    if os.path.exists("bl.json"):
        with open("bl.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_blacklist(data):
    with open("bl.json", "w") as f:
        json.dump(data, f, indent=2)


# ===== Ambil user ID + mention =====
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


# ===== Add Blacklist =====
@BOT.COMMAND("dor")
@BOT.OWNER
async def add_blacklist_func(client, message):
    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "Please mention a user, reply to their message, or provide a valid user ID.")
        return

    blacklist = load_blacklist()
    if str(user_id) in [str(uid) for uid in blacklist]:
        await notification(message, f"{user_mention} sudah ada di blacklist.")
        return

    blacklist.append(str(user_id))
    save_blacklist(blacklist)
    await notification(message, f"✅ {user_mention} berhasil ditambahkan ke blacklist.")


# ===== Remove Blacklist =====
@BOT.COMMAND("undor")
@BOT.OWNER
async def remove_blacklist_func(client, message):
    user_id, user_mention = await get_user_id_and_mention(client, message)
    if not user_id:
        await notification(message, "Please mention a user, reply to their message, or provide a valid user ID.")
        return

    blacklist = load_blacklist()
    if str(user_id) not in [str(uid) for uid in blacklist]:
        await notification(message, f"{user_mention} tidak ada di blacklist.")
        return

    blacklist = [uid for uid in blacklist if str(uid) != str(user_id)]
    save_blacklist(blacklist)
    await notification(message, f"✅ {user_mention} berhasil dihapus dari blacklist.")


# ===== List Blacklist =====
@BOT.COMMAND("listdor")
@BOT.OWNER
async def list_blacklist_func(client, message):
    blacklist = load_blacklist()
    if not blacklist:
        await notification(message, "⚠️ Tidak ada user dalam blacklist.")
        return

    text = "🚫 Blacklisted Users:\n"
    for uid in blacklist:
        try:
            user = await client.get_users(int(uid))
            text += f" - {user.mention}\n"
        except Exception:
            text += f" - <code>{uid}</code>\n"

    await message.reply(f"<blockquote>{text}</blockquote>")
