from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from .strings import get_string
from revoratebot.models import User, Department, CommentTemplate, Company
from typing import List

_default_value = ReplyKeyboardMarkup(resize_keyboard=True)
_default_value.add('no_keyboard')


def _create_keyboard(row_width=3):
    return ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)


def get_keyboard(key, language='ru'):
    if key == 'remove':
        return ReplyKeyboardRemove()
    elif key == 'registration.languages':
        language_keyboard = _create_keyboard(row_width=1)
        language_keyboard.add(get_string('languages.ru', language),
                              get_string('languages.en', language))
        return language_keyboard
    elif key == 'settings':
        settings_keyboard = _create_keyboard(row_width=1)
        settings_keyboard.add(get_string('settings.languages', language))
        settings_keyboard.add(get_string('go_back', language))
        return settings_keyboard
    elif key == 'estimates.estimates':
        estimates_keyboard = _create_keyboard(row_width=1)
        estimates_keyboard.add(get_string('estimates.value_5', language),
                               get_string('estimates.value_4', language),
                               get_string('estimates.value_3', language),
                               get_string('estimates.value_2', language),
                               get_string('estimates.value_1', language),
                               get_string('go_back', language))
        return estimates_keyboard
    elif key == 'sos.confirm':
        sos_keyboard = _create_keyboard(row_width=1)
        sos_button = KeyboardButton(get_string('sos.send_signal', language), request_location=True)
        sos_keyboard.add(sos_button)
        sos_keyboard.add(get_string('go_back', language))
        return sos_keyboard
    elif key == 'go_back':
        go_back_keyboard = _create_keyboard(row_width=1)
        go_back_keyboard.add(get_string('go_back', language))
        return go_back_keyboard
    else:
        return _default_value


def get_main_keyboard_by_user_role(user: User):
    language = user.language
    drivers_code = Department.DefaultNames.DRIVERS
    if user.department:
        keyboard = _create_keyboard(row_width=1)
        keyboard.add(get_string('menu.put_estimate', language))
        if user.department.code_name == drivers_code:
            sos_button = KeyboardButton(get_string('menu.sos', language))
            keyboard.add(sos_button)
    else:
        if not user.is_manager:
            return None
        keyboard = _create_keyboard(row_width=1)
        keyboard.add(get_string('menu.ratings', language))
    keyboard.add(get_string('menu.settings', language))
    return keyboard


def keyboard_by_user_language(user: User) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=1)
    if user.language != 'ru':
        keyboard.add(get_string('languages.ru'))
    if user.language != 'en':
        keyboard.add(get_string('languages.en'))
    keyboard.add(get_string('go_back', user.language))
    return keyboard


def keyboard_from_departments_list(departments: List[Department], language) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=3)
    departments_name = [d.name for d in departments]
    keyboard.add(*departments_name)
    keyboard.add(get_string('go_back', language))
    return keyboard


def keyboard_from_users_list(users: List[User], language) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=2)
    users_names = [u.name for u in users]
    keyboard.add(*users_names)
    keyboard.add(get_string('go_back', language))
    return keyboard

def keyboard_from_companies_list(companies: List[Company], language) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=2)
    companies_names = [c.name for c in companies]
    keyboard.add(*companies_names)
    keyboard.add(get_string('go_back', language))
    return keyboard


def keyboard_from_comments_templates(templates: List[CommentTemplate], language) -> ReplyKeyboardMarkup:
    keyboard = _create_keyboard(row_width=1)
    if language == 'en':
        templates_texts = [t.text_en for t in templates]
    elif language == 'uz':
        templates_texts = [t.text_uz for t in templates]
    else:
        templates_texts = [t.text_ru for t in templates]
    keyboard.add(*templates_texts)
    keyboard.add(get_string('go_back', language))
    return keyboard
