import time
import platform
from main.helpers.utils.handler import BOT

# Simpan waktu bot mulai
START_TIME = time.time()


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


@BOT.COMMAND("ping")
async def _(client, message):
    start = time.time()
    m = await message.reply_text("🏓 Pong...")
    end = time.time()
    ping_time = round((end - start) * 1000, 2)

    uptime = get_readable_time(time.time() - START_TIME)
    system = platform.system()
    release = platform.release()

    await m.edit_text(
        f"🏓 <b>Pong!</b>\n\n"
        f"⚡ <b>Ping:</b> <code>{ping_time} ms</code>\n"
        f"⏳ <b>Uptime:</b> <code>{uptime}</code>\n"
        f"💻 <b>System:</b> <code>{system} {release}</code>"
    )
