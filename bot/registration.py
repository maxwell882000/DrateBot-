"""
Logic for registration users in bot
"""
from . import telegram_bot
from core.managers import users
from telebot.types import Message
from resources import keyboards, strings


@telegram_bot.message_handler(commands=['start'])
def start_handler(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    def not_allowed():
        not_allowed_message = strings.get_string('registration.not_allowed')
        remove_keyboard = keyboards.get_keyboard('remove')
        telegram_bot.send_message(chat_id, not_allowed_message, reply_markup=remove_keyboard)

    current_user = users.get_user_by_telegram_id(user_id)
    if current_user:
        main_menu_keyboard = keyboards.get_main_keyboard_by_user_role(current_user)
        answer_text = strings.get_string('registration.user_exists',
                                         current_user.language).format(name=current_user.name)
        telegram_bot.send_message(chat_id, answer_text, reply_markup=main_menu_keyboard, parse_mode='HTML')
        return
    msg_text = message.text
    message_text_parts = msg_text.split(' ')
    try:
        token = message_text_parts[1]
    except IndexError:
        not_allowed()
        return
    user = users.get_user_by_token(token)
    if not user:
        not_allowed()
        return
    confirmation_result = users.confirm_user(user, user_id)
    if confirmation_result is True:
        if user.is_manager:
            welcome_message = strings.get_string('registration.welcome_manager').format(name=user.name)
        else:
            welcome_message = strings.get_string('registration.welcome_common').format(name=user.name)
        telegram_bot.send_message(chat_id, welcome_message, parse_mode='HTML')
        language_message = strings.get_string('registration.languages')
        language_keyboard = keyboards.get_keyboard('registration.languages')
        telegram_bot.send_message(chat_id, language_message, reply_markup=language_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, language_processor, user=user)
        pass
    else:
        not_allowed()
        return


def language_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    chat_id = message.chat.id
    language_ru = strings.get_string('languages.ru')
    language_en = strings.get_string('languages.en')
    language_uz = strings.get_string('languages.uz')

    def error():
        error_msg = strings.get_string('registration.languages')
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, language_processor, user=user)

    if not message.text:
        error()
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
    main_menu_keyboard = keyboards.get_main_keyboard_by_user_role(user)
    welcome_text = strings.get_string('registration.welcome', user.language)
    telegram_bot.send_message(chat_id, welcome_text, reply_markup=main_menu_keyboard, parse_mode='HTML')
