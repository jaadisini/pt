import json
import os
from main.helpers.utils.gibberish import gibberish
from main.helpers.utils.notification import notification
from main.database import groupdb, blockwordsdb, userdb
from main.helpers.utils.similiarity import AdvancedSimilarityChecker

similarity_checker = AdvancedSimilarityChecker(threshold=0.7)


# ==================== BLACKLIST USER (bl.json) ====================
def load_blacklist():
    if os.path.exists("bl.json"):
        with open("bl.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# ==================== BLACKLIST KATA (bl.txt) ====================
def load_word_blacklist():
    """Membaca daftar kata terlarang dari bl.txt"""
    if os.path.exists("bl.txt"):
        with open("bl.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


def save_word_blacklist(words):
    """Menyimpan ulang daftar kata ke bl.txt"""
    with open("bl.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(words))


def remove_word_from_blacklist(word: str):
    """Hapus kata tertentu dari bl.txt"""
    words = load_word_blacklist()
    new_words = [w for w in words if w.lower() != word.lower()]
    save_word_blacklist(new_words)
    return word in words


# ==================== CEK PESAN ====================
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
    if await userdb.is_blacklisted(user_id):  # fungsi global cek
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
    global_blockwords = load_word_blacklist()  # ambil juga dari bl.txt
    whitelistuser = await userdb.is_whitelisted(user_id)
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

        # cek blockwords dari database + bl.txt dengan similarity
        if any(
            similarity_checker.is_similar(word, blocked_word)
            for blocked_word in blockwords + global_blockwords
            for word in [message_text] + message_text.split()
        ):
            mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
            await message.delete()
            await notification(
                message,
                f"{mention}, Pesan anda telah dihapus karena terdeteksi sebagai broadcast."
            )
            return
