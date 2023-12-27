from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from duty.duty_collection import DutyCollection
from helpers.bot_helper import BotHelper
from helpers.config import Config
from models.person import Person
from random import randrange
from helpers.log import Log
from inspect import cleandoc


class Commands:
    __RESPONSE_TEXT = {
        'duty_already_enabled': 'Дежурства уже были подключены ранее ({date})',
        'duty_started': 'Дежурства подключены',
        'no_duty_or_not_started': 'Дежурный не назначен или дежурства не подключены для этого чата',
        'no_duty': 'Дежурный не назначен',
        'duty_stopped': 'Дежурства отключены',
        'duty_take': cleandoc('''
            [{duty_name}](tg://user?id={duty_id}) назначен дежурным

            Дополнительные действия

            Задачи дежурного:
            - Задача1
            - Задача2
            '''),
        'person_duty_since': '[{duty_name}](tg://user?id={duty_id}) дежурит с {date}',
        'call01': '[{duty_name}](tg://user?id={duty_id}), срочно подойдите в кабинет [{chat_title}]({message_link})',
        'call02': '[{duty_name}](tg://user?id={duty_id}), у нас труп! Возможно, криминал! По коням! [{chat_title}]({message_link})',
        'call03': '[{duty_name}](tg://user?id={duty_id}), без тебя вообще никак [{chat_title}]({message_link})',
        'history': '{history}',
        'chat': '[{chat_title}](https://t.me/c/{chat_id})\n'
    }

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug(f'Invoked start command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id):
            text = Commands.__RESPONSE_TEXT.get('duty_already_enabled').format(
                date=DutyCollection.get_duty(duty_chat_id).start_date)
        else:
            DutyCollection.init_duty(duty_chat_id)
            Log.logger.info(f'Duty started for {duty_chat_id}')
            text = Commands.__RESPONSE_TEXT.get('duty_started')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text)

    @staticmethod
    async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked stop command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id):
            DutyCollection.delete_duty(duty_chat_id)
            Log.logger.info(f'Duty stopped for {duty_chat_id}')
            text = Commands.__RESPONSE_TEXT.get('duty_stopped')
        else:
            text: str = Commands.__RESPONSE_TEXT.get('no_duty_or_not_started')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text)

    @staticmethod
    async def who(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked who command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id) and DutyCollection.get_duty(
                duty_chat_id).person:
            duty = DutyCollection.get_duty(duty_chat_id)
            text = Commands.__RESPONSE_TEXT.get('person_duty_since').format(
                duty_name=duty.person.name,
                duty_id=duty.person.telegram_id,
                date=duty.update_date)
        else:
            text: str = Commands.__RESPONSE_TEXT.get('no_duty_or_not_started')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    async def take(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked take command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id):
            duty = DutyCollection.get_duty(duty_chat_id)
            duty.person = Person(update.effective_user.id, update.effective_user.name)
            DutyCollection.update_duty(duty_chat_id, duty)
            Log.logger.info(f'Duty for {duty_chat_id} taken by {duty.person.name}:{duty.person.telegram_id}')
            text = Commands.__RESPONSE_TEXT.get('duty_take').format(
                duty_name=duty.person.name,
                duty_id=duty.person.telegram_id,
                date=duty.update_date)
        else:
            text = Commands.__RESPONSE_TEXT.get('no_duty_or_not_started')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    async def call(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked call command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id) and DutyCollection.get_duty(
                duty_chat_id).person:
            chat_id = Config.telegram_engineers_chat
            Log.logger.info(f'Duty call from {update.effective_chat.title}:{update.effective_chat.id}')
            text = Commands.__RESPONSE_TEXT.get(f'call0{randrange(start=1, stop=4, step=1)}').format(
                duty_name=DutyCollection.get_duty(duty_chat_id).person.name,
                duty_id=DutyCollection.get_duty(duty_chat_id).person.telegram_id,
                chat_title=update.effective_chat.title,
                message_link=update.effective_message.link)
        else:
            chat_id = update_chat_id
            text: str = Commands.__RESPONSE_TEXT.get('no_duty')
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked help command')
        update_chat_id = update.effective_chat.id
        message = ''
        for command, v in BotHelper.BOT_COMMANDS.items():
            message += f'/{command} - {v.get("description")}\n\n'
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=message
        )

    @staticmethod
    async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked history command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id) and DutyCollection.get_duty(
                duty_chat_id).person:
            text = ''
            for item in DutyCollection.get_duty(duty_chat_id).duty_history:
                text += f'[{item.get("person").name}](tg://user?id={item.get("person").telegram_id}) {item.get("datetime").strftime("%d.%m.%Y %H:%M")}\n'
            text = Commands.__RESPONSE_TEXT.get('history').format(
                history=text)
        else:
            text: str = Commands.__RESPONSE_TEXT.get('no_duty')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )

    @staticmethod
    async def chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        Log.logger.debug('Invoked chats command')
        update_chat_id = update.effective_chat.id
        duty_chat_id = Config.telegram_engineers_chat
        if DutyCollection.has_duty(duty_chat_id) and DutyCollection.get_duty(
                duty_chat_id).person:
            text = ''
            for chat_id in Config.telegram_duty_chats:
                chat = await context.bot.get_chat(chat_id)
                text += Commands.__RESPONSE_TEXT.get('chat').format(
                    chat_title=chat.title,
                    chat_id=str(chat_id).replace("-100", "")
                )

        else:
            text: str = Commands.__RESPONSE_TEXT.get('no_duty')
        await context.bot.send_message(
            chat_id=update_chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )
