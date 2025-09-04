from main.helpers.utils.notification import notification
from main.helpers.utils.parser import command_parser
from main.helpers.utils.handler import BOT
from main.database import userdb  # instance dari UsersDB


# ===== Ambil banyak user ID + mention =====
async def get_users_from_message(client, message):
    user_ids = []
    user_mentions = []

    # kalau reply
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_ids.append(user_id)
        user_mentions.append(message.reply_to_message.from_user.mention)

    # ambil argumen (bisa banyak dipisah spasi)
    args = command_parser(message).split()
    for arg in args:
        uid = None
        mention = None
        if arg.isdigit():  # user id
            uid = int(arg)
            try:
                user = await client.get_users(uid)
                mention = user.mention
            except Exception:
                mention = f"<code>{uid}</code>"
        else:  # username
            try:
                user = await client.get_users(arg)
                uid = user.id
                mention = user.mention
            except Exception:
                continue

        if uid and uid not in user_ids:
            user_ids.append(uid)
            user_mentions.append(mention)

    return user_ids, user_mentions


# ===== Add Global Blacklist =====
@BOT.COMMAND("dor")
@BOT.ADMIN
async def add_global_blacklist(client, message):
    user_ids, user_mentions = await get_users_from_message(client, message)
    if not user_ids:
        await notification(message, "⚠️ Harap reply, mention, username, atau beri user ID.")
        return

    added, skipped = [], []
    for uid, mention in zip(user_ids, user_mentions):
        already_blacklisted = await userdb.is_blacklisted(uid)
        if already_blacklisted:
            skipped.append(mention)
        else:
            await userdb.add_to_blacklist(uid)
            added.append(mention)

    text = ""
    if added:
        text += "✅ Ditambahkan ke blacklist global:\n" + "\n".join(added) + "\n"
    if skipped:
        text += "⚠️ Sudah ada di blacklist global:\n" + "\n".join(skipped)

    await notification(message, text)


# ===== Remove Global Blacklist =====
@BOT.COMMAND("undor")
@BOT.ADMIN
async def remove_global_blacklist(client, message):
    user_ids, user_mentions = await get_users_from_message(client, message)
    if not user_ids:
        await notification(message, "⚠️ Harap reply, mention, username, atau beri user ID.")
        return

    removed, not_found = [], []
    for uid, mention in zip(user_ids, user_mentions):
        already_blacklisted = await userdb.is_blacklisted(uid)
        if not already_blacklisted:
            not_found.append(mention)
        else:
            await userdb.remove_from_blacklist(uid)
            removed.append(mention)

    text = ""
    if removed:
        text += "✅ Dihapus dari blacklist global:\n" + "\n".join(removed) + "\n"
    if not_found:
        text += "⚠️ Tidak ada di blacklist global:\n" + "\n".join(not_found)

    await notification(message, text)


# ===== List Global Blacklist =====
@BOT.COMMAND("listdor")
@BOT.ADMIN
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
