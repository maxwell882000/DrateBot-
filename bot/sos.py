from . import telegram_bot
from .utils import Access, Helpers, Navigation
from resources import strings, keyboards
from telebot.types import Message
from core.managers import users, sos, companies


def _to_select_department(user, chat_id):
    departments_message = strings.get_string('sos.select_department', user.language)
    departments = companies.get_all_departments()
    departments_keyboard = keyboards.keyboard_from_departments_list(departments, user.language)
    telegram_bot.send_message(chat_id, departments_message, reply_markup=departments_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, departments_select_processor, user=user)


@telegram_bot.message_handler(content_types=['text'], func=Access.sos)
def sos_handler(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user = users.get_user_by_telegram_id(user_id)

    _to_select_department(user, chat_id)


def departments_select_processor(message: Message, **kwargs):
    chat_id = message.chat.id
    user = kwargs.get('user')
    
    def error():
        error_message = strings.get_string('sos.select_department', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, departments_select_processor, user=user)
    
    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        Navigation.to_main_menu(user, chat_id)
        return
    department_name = message.text
    confirm_message = strings.get_string('sos.confirm', user.language)
    confirm_keyboard = keyboards.get_keyboard('sos.confirm', user.language)
    telegram_bot.send_message(chat_id, confirm_message, reply_markup=confirm_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, confirmation_processor, user=user, department_name=department_name)


def confirmation_processor(message: Message, **kwargs):
    chat_id = message.chat.id
    user = kwargs.get('user')
    department_name = kwargs.get('department_name')

    def error():
        error_message = strings.get_string('sos.confirm', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, confirmation_processor, user=user, department_name=department_name)
    
    if message.text:
        if strings.get_string('go_back', user.language) in message.text:
            _to_select_department(user, chat_id)
            return
        else:
            error()
            return
    elif message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        sos_signal = sos.create_sos(user, latitude, longitude, department_name)
        success_message = strings.get_string('sos.success', user.language).format(department_name)
        Navigation.to_main_menu(user, chat_id, success_message)
        Helpers.send_sos_signal_to_managers(sos_signal, user)
    else:
        error()
        return
