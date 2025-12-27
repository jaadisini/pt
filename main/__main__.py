import asyncio
import signal
import sys
from importlib import import_module

import tornado.ioloop
import tornado.platform.asyncio
from pyrogram import idle
from pyrogram.errors import FloodWait

from main import bot
from main.plugins import load_modules
from main.helpers.utils.logging import LOGGER
from config import CBOT

HELP_COMMANDS = {}


async def shutdown(loop):
    LOGGER("main").info("» Stopping Bot ..")

    # 1. Stop Pyrogram cleanly
    try:
        await bot.stop()
    except Exception as e:
        LOGGER("main").error(f"Error stopping bot: {e}")

    # 2. Cancel remaining tasks (exclude current)
    tasks = [
        t for t in asyncio.all_tasks(loop)
        if t is not asyncio.current_task()
    ]

    LOGGER("main").info(f"» Cancelling {len(tasks)} tasks ..")
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    LOGGER("main").info("» Bot stopped cleanly")


async def load_module(module):
    try:
        imported_module = import_module(f"main.plugins.{module}")

        if getattr(imported_module, "__MODULE__", None):
            if getattr(imported_module, "__HELP__", None):
                HELP_COMMANDS[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module

        LOGGER("main").info(f"Successfully loaded module: {module}")

    except Exception as e:
        LOGGER("main").error(f"Failed to load module {module}: {e}")


async def load_plugins():
    modules = load_modules()
    tasks = [asyncio.create_task(load_module(m)) for m in modules]
    await asyncio.gather(*tasks)

    await bot.send_message(
        CBOT.LOG_GROUP_ID,
        f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]"
    )

    LOGGER("main").info(
        f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]"
    )


async def start_bot():
    LOGGER("main").info("» REPO BY : @NakamaMarket ..")

    try:
        await bot.start()
        await load_plugins()

    except FloodWait as e:
        wait_time = int(e.value)
        LOGGER("main").error(f"FloodWait for {wait_time} seconds")

        for i in range(wait_time, 0, -1):
            sys.stdout.write(f"\r» Wait for {i} seconds ..")
            sys.stdout.flush()
            await asyncio.sleep(1)

        print()
        await bot.start()


async def main():
    loop = asyncio.get_running_loop()

    # Signal handler
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            s, lambda: asyncio.create_task(shutdown(loop))
        )

    await start_bot()

    try:
        await idle()
    finally:
        await shutdown(loop)


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER("main").info("\nBot Stopped!")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
