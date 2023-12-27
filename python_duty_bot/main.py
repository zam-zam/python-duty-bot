from bot.telegram_bot import TelegramBot
from helpers.config import Config


if __name__ == '__main__':
    TelegramBot(Config.telegram_bot_token).run()
