from main import bot
import asyncio

async def notification(message, text):
    await message.delete()
    notification_text = f"<blockquote>⚠️ **Peringatan {text}**</blockquote>"
    notification_send = await bot.send_message(message.chat.id, notification_text)
    await asyncio.sleep(1)
    return await notification_send.delete()
    
