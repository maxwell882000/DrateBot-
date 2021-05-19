"""
Main logic for Telegram Bot
"""
from telebot import TeleBot
from Revorate import settings as app_settings
from telebot.types import Message
from resources import strings, keyboards
from core.managers import users


telegram_bot = TeleBot(app_settings.API_TOKEN)

from . import registration, estimates, managers, settings, sos
from .utils import Navigation

@telegram_bot.message_handler(content_type=['text'], func=lambda m: m.chat.type == 'private')
def empty_message(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    def not_allowed():
        not_allowed_message = strings.get_string('registration.not_allowed')
        remove_keyboard = keyboards.get_keyboard('remove')
        telegram_bot.send_message(chat_id, not_allowed_message, reply_markup=remove_keyboard)
    
    current_user = users.get_user_by_telegram_id(user_id)
    if current_user:
        Navigation.to_main_menu(current_user, chat_id)
    else:
        not_allowed()
