from os import environ
from dotenv import load_dotenv
from typing import List

load_dotenv()


class Config:
    log_level: str = environ.get("LOG_LEVEL", "INFO")

    data_dir: str = environ.get("DATA_DIR", "data")

    startup_check_delay_seconds: int = int(environ.get("STARTUP_CHECK_DELAY_SECONDS", 5))
    startup_check_file: str = environ.get("STARTUP_CHECK_FILE", "/tmp/start")

    telegram_bot_token: str = environ.get("TELEGRAM_BOT_TOKEN")
    telegram_bot_username: str = environ.get("TELEGRAM_BOT_USERNAME")

    telegram_engineers_chat: int = int(environ.get("TELEGRAM_ENGINEERS_CHAT"))
    telegram_duty_chats: List[int] = list(map(int, environ["TELEGRAM_DUTY_CHATS"].split(",")))
    
    telegram_admins: List[int] = list(map(int, environ["TELEGRAM_ADMINS"].split(",")))
