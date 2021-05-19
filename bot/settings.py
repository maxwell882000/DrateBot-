from . import telegram_bot
from .utils import Access, Navigation
from resources import strings, keyboards
from core.managers import users
from telebot.types import Message


@telegram_bot.message_handler(content_types=['text'], func=Access.settings)
def settings_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = users.get_user_by_telegram_id(user_id)

    Navigation.to_settings(user, chat_id)


def settings_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    chat_id = message.chat.id

    def error():
        error_message = strings.get_string('settings.menu', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, settings_processor, user=user)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        Navigation.to_main_menu(user, chat_id)
    elif strings.get_string('settings.languages', user.language) in message.text:
        languages_message = strings.get_string('settings.select_language', user.language)
        languages_keyboard = keyboards.keyboard_by_user_language(user)
        telegram_bot.send_message(chat_id, languages_message, reply_markup=languages_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, languages_processor, user=user)
    else:
        error()
        return


def languages_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    chat_id = message.chat.id
    language_ru = strings.get_string('languages.ru')
    language_en = strings.get_string('languages.en')
    language_uz = strings.get_string('languages.uz')

    def error():
        error_message = strings.get_string('settings.select_language', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, languages_processor, user=user)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        Navigation.to_settings(user, chat_id)
        return
    if language_ru in message.text:
        language = 'ru'
    elif language_en in message.text:
        language = 'en'
    elif language_uz in message.text:
        language = 'uz'
    else:
        error()
        return
    users.set_user_language(user, language)
    success_message = strings.get_string('settings.languages_success', user.language)
    settings_keyboard = keyboards.get_keyboard('settings', user.language)
    telegram_bot.send_message(chat_id, success_message, reply_markup=settings_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, settings_processor, user=user)
