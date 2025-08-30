from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS

from main import bot
from config import COWNER

class BOT:

    @staticmethod
    def COMMAND(command, filter=None):
        def wrapper(func):
            message_filters = (
                filters.command(command) & filter
                if filter
                else filters.command(command)
            )

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper
    
    @staticmethod
    def ADMIN(func):
        async def wrapper(client, message):
            admin = await client.get_chat_member(message.chat.id, message.from_user.id)
            if admin.status in [CMS.OWNER, CMS.ADMINISTRATOR]:
                return await func(client, message)
        return wrapper
    
    @staticmethod
    def NONADMIN(func):
        async def wrapper(client, message):
            user_id = message.from_user.id
            if user_id == COWNER.OWNER_ID:
                return
            admin = await client.get_chat_member(message.chat.id, user_id)
            if admin.status in [CMS.OWNER, CMS.ADMINISTRATOR]:
                return
            return await func(client, message)
        
        return wrapper

    @staticmethod
    def ONMESSAGE(filter=None):
        def wrapper(func):
            message_filters = filter

            @bot.on_message(message_filters)
            async def wrapped_func(client, message):
                if message.text and message.text.startswith("/"):
                    return
                return await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def CALLBACK(command):
        def wrapper(func):
            @bot.on_callback_query(filters.regex(command))
            async def wrapped_func(client, message):
                await func(client, message)

            return wrapped_func

        return wrapper

    @staticmethod
    def OWNER(func):
        async def function(client, message):
            user_id = message.from_user.id
            if user_id == COWNER.OWNER_ID:
                await func(client, message)

        return function
