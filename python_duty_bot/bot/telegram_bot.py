from telegram.ext import CommandHandler, MessageHandler, Application

from bot.commands import Commands
from helpers.bot_helper import BotHelper
from helpers.log import Log
from helpers.config import Config

from telegram.ext import ContextTypes


class TelegramBot:
    def __init__(self, token: str):
        self.__application: Application = Application.builder().token(token).connection_pool_size(8).connect_timeout(10.0).read_timeout(10.0).build()

    def bind_commands(self) -> None:
        for command, v in BotHelper.BOT_COMMANDS.items():
            self.__application.add_handler(CommandHandler(command=command,
                                                          callback=getattr(Commands, v.get('function')),
                                                          filters=v.get('filter')))
        Log.logger.debug('Bot command handlers bound')
        for message, v in BotHelper.BOT_MESSAGES.items():
            self.__application.add_handler(MessageHandler(filters=v.get('filter'),
                                                          callback=getattr(Commands, v.get('function'))))
        Log.logger.debug('Bot message handlers bound')

    async def startup_check(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.application.bot.get_me()
        with open(Config.startup_check_file, 'w') as f:
            f.write('Bot started')
            Log.logger.info('Bot started')

    def run(self) -> None:
        self.bind_commands()
        job_queue = self.__application.job_queue
        job_queue.run_once(self.startup_check, Config.startup_check_delay_seconds)
        self.__application.run_polling()
