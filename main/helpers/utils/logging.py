import logging
from logging.handlers import RotatingFileHandler
from functools import wraps

from config import CBOT

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(CBOT.LOG_FILE_NAME, maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

def print_and_log(func):
    @wraps(func)
    def wrapper(self, msg, *args, **kwargs):
        print(f"[{self.name}] {msg}")
        return func(self, msg, *args, **kwargs)
    return wrapper

class PrintLogger(logging.Logger):
    @print_and_log
    def info(self, msg, *args, **kwargs):
        super().info(msg, *args, **kwargs)

    @print_and_log
    def warning(self, msg, *args, **kwargs):
        super().warning(msg, *args, **kwargs)

    @print_and_log
    def error(self, msg, *args, **kwargs):
        super().error(msg, *args, **kwargs)

    @print_and_log
    def critical(self, msg, *args, **kwargs):
        super().critical(msg, *args, **kwargs)

    @print_and_log
    def debug(self, msg, *args, **kwargs):
        super().debug(msg, *args, **kwargs)

logging.setLoggerClass(PrintLogger)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)