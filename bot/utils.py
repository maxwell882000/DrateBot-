from telebot.types import Message
from telebot.apihelper import ApiException
from core.managers import users
from revoratebot.models import User, Department, SosSignal, Rating
from resources import strings, keyboards
from typing import Optional
from . import telegram_bot
import time


class Access:

    @staticmethod
    def _auth(message: Message) -> Optional[User]:
        user_id = message.from_user.id
        user = users.get_user_by_telegram_id(user_id)
        if not user:
            return None
        return user

    @staticmethod
    def _private(message: Message):
        return message.chat.type != 'group' and message.chat.type != 'supergroup'

    @staticmethod
    def settings(message: Message):
        if not message.text:
            return False
        user = Access._auth(message)
        if not user:
            return False
        return Access._private(message) and strings.get_string('menu.settings', user.language) in message.text

    @staticmethod
    def estimates(message: Message):
        if not message.text:
            return False
        user = Access._auth(message)
        if not user:
            return False
        if user.is_manager:
            return False
        if user.department.code_name != Department.DefaultNames.DRIVERS:
            return False
        return Access._private(message) and strings.get_string('menu.put_estimate', user.language) in message.text

    @staticmethod
    def sos(message: Message):
        if not message.text:
            return False
        user = Access._auth(message)
        if not user:
            return False
        if user.is_manager:
            return False
        if user.department.code_name != Department.DefaultNames.DRIVERS:
            return False
        return Access._private(message) and strings.get_string('menu.sos', user.language) in message.text
    
    @staticmethod
    def ratings(message: Message):
        if not message.text:
            return False
        user = Access._auth(message)
        if not user:
            return False
        if not user.is_manager:
            return False
        return Access._private(message) and strings.get_string('menu.ratings', user.language) in message.text


class Navigation:
    @staticmethod
    def to_main_menu(user, chat_id, message_text=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('menu.common', user.language)
        menu_keyboard = keyboards.get_main_keyboard_by_user_role(user)
        telegram_bot.send_message(chat_id, menu_message, reply_markup=menu_keyboard, parse_mode='HTML')

    @staticmethod
    def to_settings(user, chat_id):
        from .settings import settings_processor
        settings_message = strings.get_string('settings.menu', user.language)
        settings_keyboard = keyboards.get_keyboard('settings', user.language)
        telegram_bot.send_message(chat_id, settings_message, reply_markup=settings_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, settings_processor, user=user)


class Helpers:
    @staticmethod
    def send_sos_signal_to_managers(sos_signal: SosSignal, sender: User):
        managers = users.get_registered_managers()
        for manager in managers:
            if len(managers) > 10:
                time.sleep(0.1)
            sos_message = strings.string_from_sos_signal(sos_signal, sender, manager.language)
            try:
                telegram_bot.send_message(manager.telegram_user_id, sos_message, parse_mode='HTML')
                telegram_bot.send_location(manager.telegram_user_id, sos_signal.location_lat, sos_signal.location_lon)
            except ApiException:
                pass

    @staticmethod
    def send_bad_rating_to_managers(rating: Rating, sender: User, reciever: User):
        managers = users.get_registered_managers()
        for manager in managers:
            if len(managers) > 10:
                time.sleep(0.1)
            rating_message = strings.string_from_rating(rating, sender, reciever, manager.language)
            try:
                telegram_bot.send_message(manager.telegram_user_id, rating_message, parse_mode='HTML')
            except ApiException:
                pass
