import json
import os
from main.helpers.utils.gibberish import gibberish
from main.helpers.utils.notification import notification
from main.database import groupdb, blockwordsdb, userdb
from main.helpers.utils.similiarity import AdvancedSimilarityChecker

similarity_checker = AdvancedSimilarityChecker(threshold=0.7)


# Load daftar blacklist dari bl.json (GLOBAL)
def load_blacklist():
    if os.path.exists("bl.json"):
        with open("bl.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


async def message_func(client, message):
    if not message.from_user:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # ==== Cek Global Blacklist (bl.json) ====
    blacklist = load_blacklist()
    if str(user_id) in [str(uid) for uid in blacklist]:
        mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        await message.delete()
        await notification(
            message,
            f"{mention}, Pesan anda telah dihapus karena terdeteksi sebagai broadcast."
        )
        return

    # ==== Cek Blacklist dari database (GLOBAL, bukan per grup) ====
    if await userdb.is_blacklisted_global(user_id):  # fungsi global cek
        mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        await message.delete()
        await notification(
            message,
            f"{mention}, Pesan anda telah dihapus karena terdeteksi sebagai broadcast."
        )
        return

    # ==== Anti Broadcast / Blockwords (per grup) ====
    state_group = await groupdb.get_antibc_state(chat_id)
    blockwords = await blockwordsdb.get_blockwords(chat_id)
    whitelistuser = await userdb.is_whitelisted(chat_id, user_id)
    message_text = message.text or ""

    if state_group and not whitelistuser:
        # cek gibberish
        if gibberish(message):
            mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
            await message.delete()
            await notification(
                message,
                f"{mention}, Pesan anda telah dihapus karena terdeteksi sebagai broadcast."
            )
            return

        # cek blockwords dengan similarity
        if any(
            similarity_checker.is_similar(word, blocked_word)
            for blocked_word in blockwords
            for word in [message_text] + message_text.split()
        ):
            mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
            await message.delete()
            await notification(
                message,
                f"{mention}, Pesan anda telah dihapus karena terdeteksi sebagai broadcast."
            )
            return
