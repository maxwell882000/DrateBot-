from bot import telegram_bot
from core.managers import users
from resources import strings
from telebot.apihelper import ApiException
import time


def notify_users_about_estimates():
    confirmed_users = users.get_confirmed_users()
    for user in confirmed_users:
        notify_message = strings.get_string('notifications.message', user.language)
        try:
            telegram_bot.send_message(user.telegram_user_id, notify_message)
        except ApiException:
            pass
        time.sleep(0.1)
