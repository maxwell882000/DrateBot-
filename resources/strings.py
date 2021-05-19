import os
import json
from revoratebot.models import Rating, SosSignal


_basedir = os.path.abspath(os.path.dirname(__file__))

# Load strings from json
# Russian language
_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r', encoding='utf8').read())

# Uzbek language
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r', encoding='utf8').read())

# English language
_strings_en = json.loads(open(os.path.join(_basedir, 'strings_en.json'), 'r', encoding='utf8').read())


def get_string(key, language='ru'):
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    elif language == 'en':
        return _strings_en.get(key, 'no_string')
    else:
        raise Exception('Invalid language')


def string_from_estimate_value(value: int, langauge):
    return get_string('estimates.value_{}'.format(value), langauge)


def estimate_value_from_string(string, language):
    if get_string('estimates.value_1', language) in string:
        return Rating.Values.VERY_LOW
    elif get_string('estimates.value_2', language) in string:
        return Rating.Values.LOW
    elif get_string('estimates.value_3', language) in string:
        return Rating.Values.MEDIUM
    elif get_string('estimates.value_4', language) in string:
        return Rating.Values.HIGH
    elif get_string('estimates.value_5', language) in string:
        return Rating.Values.VERY_HIGH
    else:
        return None


def string_from_sos_signal(sos_signal: SosSignal, sender, language):
    datetime = sos_signal.created_at.strftime('%d.%m.%Y %H:%M')
    sos_message_content = ""
    sos_message_content += get_string('sos.new_signal', language)
    sos_message_content += '\n'
    sos_message_content += get_string('sos.sender', language).format(name=sender.name, phone=sender.phone_number)
    sos_message_content += '\n'
    sos_message_content += get_string('sos.department_name', language).format(sos_signal.department_name)
    sos_message_content += '\n'
    sos_message_content += get_string('sos.sent_at', language).format(date=datetime)
    return sos_message_content


def string_from_rating(rating: Rating, sender, reciever, language):
    datetime = rating.created_at.strftime('%d.%m.%Y %H:%M')
    rating_message_content = ""
    rating_message_content += string_from_estimate_value(rating.value, language)
    rating_message_content += "\n"
    rating_message_content += get_string('ratings.from_user', language).format(name=sender.name,
                                                                               phone=sender.phone_number,
                                                                               department=sender.department.name)
    rating_message_content += get_string('ratings.to_user', language).format(name=reciever.name,
                                                                             phone=reciever.phone_number,
                                                                             department=reciever.department.name)
    rating_message_content += get_string('ratings.created_at', language).format(datetime)
    if rating.comment:
        rating_message_content += '\n'
        rating_message_content += get_string('ratings.comment', language).format(rating.comment)
    return rating_message_content
