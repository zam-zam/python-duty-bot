from telegram.ext import filters
from telegram import MessageEntity
from helpers.config import Config


class BotHelper:
    BOT_COMMANDS = {
        'start': {
            'description': 'Подключить дежурства для этого чата',
            'function': 'start',
            'filter': (filters.User(Config.telegram_admins)
                        & filters.Chat(Config.telegram_engineers_chat))
        },
        'help': {
            'description': 'Показать справку',
            'function': 'help',
            'filter': filters.Chat(Config.telegram_engineers_chat)
                        | filters.Chat(Config.telegram_admins)
        },
        'who': {
            'description': 'Узнать, кто сейчас дежурит',
            'function': 'who',
            'filter': filters.Chat(Config.telegram_engineers_chat)
                        | filters.Chat(Config.telegram_admins)
        },
        'take': {
            'description': 'Принять дежурство',
            'function': 'take',
            'filter': filters.Chat(Config.telegram_engineers_chat)
        },
        'stop': {
            'description': 'Выключить дежурства и удалить все настройки',
            'function': 'stop',
            'filter': (filters.User(Config.telegram_admins)
                        & filters.Chat(Config.telegram_engineers_chat))
        },
        'history': {
            'description': f'Вывести историю дежурств',
            'function': 'history',
            'filter': filters.Chat(Config.telegram_engineers_chat)
                        | filters.Chat(Config.telegram_admins)
        },
        'chats': {
            'description': f'Вывести чаты с другими командами',
            'function': 'chats',
            'filter': filters.Chat(Config.telegram_engineers_chat)
                        | filters.Chat(Config.telegram_admins)
        }
    }
    BOT_MESSAGES = {
         'mention': {
            'description': 'Позвать дежурного',
            'function': 'call',
            'filter': (filters.Chat(Config.telegram_duty_chats)
                        & filters.UpdateType.MESSAGE
                        & filters.Entity(MessageEntity.MENTION)
                        & filters.Regex(f'@{Config.telegram_bot_username}'))
        }
    }
