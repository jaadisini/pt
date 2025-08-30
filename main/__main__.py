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
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    LOGGER("main").info("» Stop all running processes..")
    await asyncio.gather(*tasks, return_exceptions=True)
    LOGGER("main").info("» Bot stopped!")
    loop.stop()

async def load_module(module):
    try:
        imported_module = import_module(f"main.plugins.{module}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELP_COMMANDS[imported_module.__MODULE__.replace(" ", "_").lower()] = imported_module
        LOGGER("main").info(f"Successfully loaded module: {module}")
    except Exception as e:
        LOGGER("main").error(f"Failed to load module {module}: {str(e)}")

async def load_plugins():
    modules = load_modules()
    load_tasks = []

    for module in modules:
        load_tasks.append(asyncio.create_task(load_module(module)))

    await asyncio.gather(*load_tasks)

    await bot.send_message(CBOT.LOG_GROUP_ID, f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]")
    LOGGER("main").info(f"[🤖 @{bot.me.username} 🤖] [🔥 TELAH BERHASIL DIAKTIFKAN! 🔥]")

async def start_bot():
    LOGGER("main").info("» REPO BY : @NakamaMarket ..")
    try:
        await bot.start()
        await load_plugins()
    except FloodWait as e:
        wait_time = int(e.value)
        LOGGER("main").error(f"FloodWait for {wait_time} seconds")
        for remaining in range(wait_time, 0, -1):
            sys.stdout.write(f"\r» Wait for {remaining} seconds ..")
            sys.stdout.flush()
            await asyncio.sleep(1)
        LOGGER("main").info("\n» REPO BY : @NakamaMarket")
        await bot.start()

async def main():
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(loop)))
    await start_bot()
    try:
        await idle()
    except Exception as e:
        LOGGER("main").error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER("main").info("\nBot Stopped!")
        loop.run_until_complete(shutdown(loop))
    except asyncio.exceptions.CancelledError:
        pass
    finally:
        loop.close()
