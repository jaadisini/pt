from main.helpers.utils.gibberish import gibberish
from main.helpers.utils.notification import notification
from main.database import groupdb, blockwordsdb, userdb
from main.helpers.utils.similiarity import AdvancedSimilarityChecker

similarity_checker = AdvancedSimilarityChecker(threshold=0.7)


async def message_func(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    state_group = await groupdb.get_antibc_state(chat_id)
    blockwords = await blockwordsdb.get_blockwords(chat_id)
    whitelistuser = await userdb.is_whitelisted(chat_id, user_id)
    message_text = message.text or ""

    if state_group and not whitelistuser:
        # cek gibberish
        if gibberish(message):
            mention = (
                f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
                if message.from_user
                else "."
            )
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
            mention = (
                f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
                if message.from_user
                else "."
            )
            await message.delete()
            await notification(
                message,
                f"{mention}, Pesan anda telah dihapus karena mengandung kata terlarang."
            )
            return
