from . import telegram_bot
from .utils import Access, Navigation, Helpers
from core.managers import users, ratings
from core import scheduler
from resources import strings, keyboards
from telebot.types import Message


def _to_dispatchers_select(user, chat_id):
    dispatchers = users.get_dispatchers()
    if not dispatchers:
        empty_message = strings.get_string('estimates.dispatchers_empty', user.language)
        telegram_bot.send_message(chat_id, empty_message)
        return
    users_message = strings.get_string('estimates.select_user', user.language)
    users_keyboard = keyboards.keyboard_from_users_list(dispatchers, user.language)
    telegram_bot.send_message(chat_id, users_message, reply_markup=users_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, users_processor, user=user)


def _to_estimates(user, chat_id, selected_user):
    estimates_message = strings.get_string('estimates.select_estimate', user.language)
    estimates_keyboard = keyboards.get_keyboard('estimates.estimates', user.language)
    telegram_bot.send_message(chat_id, estimates_message, reply_markup=estimates_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, estimates_processor, user=user,
                                                       selected_user=selected_user)


@telegram_bot.message_handler(content_types=['text'], func=Access.estimates)
def estimates_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user = users.get_user_by_telegram_id(user_id)
    _to_dispatchers_select(user, chat_id)


def users_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    chat_id = message.chat.id

    def error():
        error_message = strings.get_string('estimates.select_user', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, users_processor, user=user)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        Navigation.to_main_menu(user, chat_id)
        return
    selected_user = users.find_dispatcher_by_name(message.text)
    if not selected_user:
        error()
        return
    _to_estimates(user, chat_id, selected_user)


def estimates_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    selected_user = kwargs.get('selected_user')
    chat_id = message.chat.id

    def error():
        error_message = strings.get_string('estimate.select_estimate', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, estimates_processor, user=user,
                                                           selected_user=selected_user)

    if not message.text:
        error()
        return
    # BUG: Go back doesn't work
    if strings.get_string('go_back', user.language) in message.text:
        _to_dispatchers_select(user, chat_id)
        return
    value = strings.estimate_value_from_string(message.text, user.language)
    if not value:
        error()
        return
    comment_message = strings.get_string('estimates.comment', user.language)
    if value < 4:
        comment_templates = selected_user.department.comment_templates.all()
        comment_message = strings.get_string('estimates.comment_with_templates', user.language)
        comments_keyboard = keyboards.keyboard_from_comments_templates(comment_templates, user.language)
    else:
        comments_keyboard = keyboards.get_keyboard('go_back', user.language)
    new_rating = ratings.create_rating(user, selected_user, value)
    scheduler.add_timer_for_comment(chat_id, new_rating.id, timer_for_comment)
    telegram_bot.send_message(chat_id, comment_message, reply_markup=comments_keyboard, parse_mode='HTML')
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, comments_processor, user=user,
                                                       selected_user=selected_user,
                                                       estimate=value, rating_id=new_rating.id)


def comments_processor(message: Message, **kwargs):
    user = kwargs.get('user')
    selected_user = kwargs.get('selected_user')
    estimate_value = kwargs.get('estimate')
    rating_id = kwargs.get('rating_id')
    chat_id = message.chat.id

    def error():
        error_message = strings.get_string('estimates.comment', user.language)
        telegram_bot.send_message(chat_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, comments_processor, user=user,
                                                           selected_user=selected_user,
                                                           estimate=estimate_value)

    if not message.text:
        error()
        return
    if strings.get_string('go_back', user.language) in message.text:
        _to_estimates(user, chat_id, selected_user)
        return
    comment = message.text
    rating = ratings.set_comment_for_rating(rating_id, comment)
    scheduler.remove_timer_for_comment(rating.id)
    success_message = strings.get_string('estimates.success', user.language).format(name=selected_user.name,
                                                                                    department=selected_user.department.name)
    Navigation.to_main_menu(user, chat_id, message_text=success_message)
    if estimate_value < 4:
        Helpers.send_bad_rating_to_managers(rating, user, selected_user)


def timer_for_comment(chat_id: int, rating_id):
    scheduler.remove_timer_for_comment(rating_id)
    rating = ratings.get_rating_by_id(rating_id)
    user = users.get_by_id(rating.from_id)
    selected_user = users.get_by_id(rating.to_id)
    if not rating:
        return
    if rating.comment:
        return
    success_message = strings.get_string('estimates.success', user.language).format(name=selected_user.name,
                                                                                    department=selected_user.department.name)
    telegram_bot.clear_step_handler_by_chat_id(chat_id)
    Navigation.to_main_menu(user, chat_id, message_text=success_message)
    if rating.value < 4:
        Helpers.send_bad_rating_to_managers(rating, user, selected_user)
    