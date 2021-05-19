from . import telegram_bot
from .utils import Access, Navigation
from core.managers import ratings, users, companies
from resources import keyboards, strings
from telebot.types import Message


def _to_companies_select(user, chat_id):
    companies_message = strings.get_string('ratings.select_company', user.language)
    all_companies = companies.get_all_companies()
    companies_keyboard = keyboards.keyboard_from_companies_list(all_companies, user.language)
    telegram_bot.send_message(chat_id, companies_message, reply_markup=companies_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, company_rating_processor, user=user)


@telegram_bot.message_handler(content_types=['text'], func=Access.ratings)
def ratings_handler(message: Message):
    chat_id = message.chat.id
    user = users.get_user_by_telegram_id(message.from_user.id)

    _to_companies_select(user, chat_id)


def company_rating_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    chat_id = message.chat.id

    def error():
        error_message = strings.get_string('ratings.select_company', language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, user=user)
    
    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        Navigation.to_main_menu(user, chat_id)
        return
    company_name = message.text
    company = companies.get_company_by_name(company_name)
    if not company:
        error()
        return
    wait_message = strings.get_string('ratings.please_wait', user.language)
    telegram_bot.send_message(chat_id, wait_message)
    ratings_img = ratings.get_img_ratings_for_company(company)
    telegram_bot.send_chat_action(chat_id, 'upload_photo')
    telegram_bot.send_photo(chat_id, open(ratings_img, 'rb'))
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, company_rating_processor, user=user)
