import re

# Existing patterns (unchanged)
EMOJI_PATTERN = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002702-\U000027B0"  # other miscellaneous symbols
    u"\U000024C2-\U0001F251"  # enclosed characters
    "]+", flags=re.UNICODE)

NONASCII_PATTERN = re.compile(r'[^\x00-\x7F\n]')
REPEATSPACE_PATTERN = re.compile(r'^(\w \b)+\w$')
FULLCAPS_PATTERN = re.compile(r'^[A-Z\s]+$')
NONSPACE_PATTERN = re.compile(r'\w{10,}')
REPEAT_PATTERN = re.compile(r'([a-zA-Z])\1{1,}')
NUMBERINMID_PATTERN = re.compile(r'[a-zA-Z]+\d+[a-zA-Z]+')

# New pattern for vertical text
VERTICAL_TEXT_PATTERN = re.compile(r'^([A-Za-z]\n){2,}[A-Za-z]$')

# Existing functions (unchanged)
def remove_emoji(text):
    return EMOJI_PATTERN.sub('', text)

def nonascii_text(text):
    return bool(text) and (NONASCII_PATTERN.search(remove_emoji(text)) is not None)

def repeatspace_text(text):
    return REPEATSPACE_PATTERN.match(text.strip()) is not None

def fullcaps_text(text):
    return FULLCAPS_PATTERN.match(text.strip()) is not None

def nonspace_text(text):
    return NONSPACE_PATTERN.search(text) is not None

def repeat_text(text):
    return bool(text) and REPEAT_PATTERN.search(text) is not None

def newline_text(text):
    return '\n' in text

def numberinmid_text(text):
    return NUMBERINMID_PATTERN.search(text) is not None

def startnonletter_text(text):
    pattern = r'^[^a-zA-Z]'
    return bool(re.match(pattern, text))

def gibberish(message):
    if not (text := message.text or message.caption):
        return False

    if len(text) < 4:
        return True

    text = text.strip()

    return (startnonletter_text(text) or
            newline_text(text) or
            fullcaps_text(text) or
            numberinmid_text(text) or
            nonspace_text(text) or
            repeatspace_text(text) or
            repeat_text(text) or
            nonascii_text(text) or
            bool(message.forward_from or message.forward_from_chat))