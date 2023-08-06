import os
import re

from emoji import emojize
from yc_event_to_json import convert
from abc import ABC, abstractmethod
from telegram_admin_informer import send_message as inform_admin

TELEGRAM_BOT_ADMIN = os.getenv('TELEGRAM_BOT_ADMIN')
PARSE_MODE = 'markdown'

re_command = re.compile(r'^/([a-z]+)(\s+(\S.*))?$')
re_emoji = re.compile(r'\:[a-z\-_]+\:')

class Event:

    unparsed = None
    chat_id = None
    username = None
    command = None
    query = None
    payload = None
    is_admin = False

    def __init__(self, body):


        query = body.get('callback_query')
        message = body.get('message') or body.get('edited_message')
        self.unparsed = not (message or query) and body
        if self.unparsed:
            return
        self.payload = query and query.get('data') or message and message.get('text')
        if self.payload:
            message_from = (query or message)['from']
            self.chat_id = message_from['id']
            self.is_admin = TELEGRAM_BOT_ADMIN and self.chat_id == TELEGRAM_BOT_ADMIN
            self.username = message_from['username']

            self.command = None
            self.query = query
            if query:
                return
            m = re.match(re_command, self.payload)
            if m:
                self.command = m.group(1)
                self.payload = m.group(3)
    
    def __str__(self):
        return f'Сообщение от {self.username} (id={self.chat_id}). Содержание: "{self.payload}". Команда: {self.command}'

    @staticmethod
    def from_request(event):
        body = convert(event)
        return Event(body)
    

class AbstractTelegramProcessor(ABC):

    def __init__(self, event, bot=None):
        if bot:
            self.bot = bot
        if not self.bot:
            raise ValueError('Бот не установлен. Воспользуйтесь конструктором или методом setup.')
        self.event = event
        self.parse_mode = PARSE_MODE
        self.answer = None
        if event.query:
            self.answer = self.process_query(event.payload, event.query)
        elif event.command:
            self.answer = self.process_command(event.payload, event.command)
        elif event.payload:
            self.answer = self.process_text(event.payload)
        else:
            self.answer = self.process_unparsed(event.unparsed)

    def reply(self):
        text, reply_markup = self.answer
        self.bot.sendMessage(
            chat_id=self.event.chat_id, 
            text=self.emojify(text), 
            parse_mode=self.parse_mode, 
            reply_markup=reply_markup
        )

    @abstractmethod
    def process_unparsed(self, body) -> tuple:
        pass

    @abstractmethod
    def process_command(self, payload, command) -> tuple:
        pass

    @abstractmethod
    def process_query(self, payload, query) -> tuple:
        pass

    @abstractmethod
    def process_text(self, payload) -> tuple:
        pass

    @classmethod
    def setup(cls, bot):
        cls.bot = bot

    @staticmethod
    def inform_admin(data):
        inform_admin(data)

    @staticmethod
    def emojify(text):
        items = set(re.findall(re_emoji, text))
        for item in list(items):
            emoji = emojize(item.replace('-', '_'))
            text = text.replace(item, emoji)
        return text


class EchoProcessor(AbstractTelegramProcessor):

    def process_unparsed(self, body) -> tuple:
        self.bot.sendMessage('Такой тип сообщений не поддерживается этим ботом.')
        raise ValueError(f'Неподдерживаемый тип сообщений: {body}')

    def process_command(self, payload, command) -> tuple:
        return (f'Command "{command}" with argument "{payload}".', None)

    def process_query(self, payload, query) -> tuple:
        return (f'Query with payload "{payload}".', None)

    def process_text(self, payload) -> tuple:
        return (f'Simple text: "{payload}".', None)
