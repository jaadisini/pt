import json
import os

from config import COWNER
from main.helpers.utils.gibberish import gibberish
from main.helpers.utils.notification import notification
from main.helpers.utils.similiarity import AdvancedSimilarityChecker
from main.database import groupdb, blockwordsdb, userdb

similarity_checker = AdvancedSimilarityChecker(threshold=0.7)


# ==================== BLACKLIST USER (bl.json) ====================

def load_blacklist() -> list:
    """Membaca daftar user ter-blacklist dari bl.json"""
    if os.path.exists("bl.json"):
        with open("bl.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# ==================== BLACKLIST KATA (bl.txt) ====================

def load_word_blacklist() -> list:
    """Membaca daftar kata terlarang dari bl.txt"""
    if os.path.exists("bl.txt"):
        with open("bl.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []


def save_word_blacklist(words: list) -> None:
    """Menyimpan ulang daftar kata ke bl.txt"""
    with open("bl.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(words))


def remove_word_from_blacklist(word: str) -> bool:
    """Hapus kata tertentu dari bl.txt"""
    words = load_word_blacklist()
    new_words = [w for w in words if w.lower() != word.lower()]
    save_word_blacklist(new_words)
    return word in words


# ==================== CEK PESAN ====================

async def message_func(client, message):
    """Cek pesan masuk: blacklist user, blacklist kata, antibc, dll"""
    if not message.from_user:
        return

    # abaikan pesan dari owner
    if message.from_user.id in COWNER.OWNER_ID:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id
    message_text = message.text or ""

    # ==== Cek Global Blacklist (bl.json) ====
    blacklist = load_blacklist()
    if str(user_id) in [str(uid) for uid in blacklist]:
        mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        await message.delete()
        await notification(
            message,
            f"{mention}, pesan anda telah dihapus karena terdeteksi sebagai broadcast."
        )
        return

    # ==== Cek Blacklist dari database (GLOBAL, bukan per grup) ====
    if await userdb.is_blacklisted(user_id):
        mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
        await message.delete()
        await notification(
            message,
            f"{mention}, pesan anda telah dihapus karena terdeteksi sebagai broadcast."
        )
        return

    # ==== Anti Broadcast / Blockwords (per grup) ====
    state_group = await groupdb.get_antibc_state(chat_id)
    blockwords = await blockwordsdb.get_blockwords(chat_id)
    global_blockwords = load_word_blacklist()
    whitelistuser = await userdb.is_whitelisted(user_id)

    if state_group and not whitelistuser:
        # cek gibberish
        if gibberish(message):
            mention = f"[{message.from_user.first_name}](tg://user?id={user_id})"
            await message.delete()
            await notification(
                message,
                f"{mention}, pesan anda telah dihapus karena terdeteksi sebagai broadcast."
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
                f"{mention}, pesan anda telah dihapus karena terdeteksi sebagai broadcast."
            )
            return
