def command_parser(message):
    if message.reply_to_message and len(message.command) < 2:
        return message.reply_to_message.text or message.reply_to_message.caption or ""
    return message.text.split(None, 1)[1] if len(message.command) > 1 else ""