from django.core.management.base import BaseCommand
from bot import telegram_bot
import telebot
import logging


class Command(BaseCommand):
    help = "Start the telegram bot without server"

    def handle(self, *args, **options):
        from bot import registration, settings, estimates, sos, managers
        from core import scheduler
        telegram_bot.remove_webhook()
        telebot.logger.setLevel(logging.DEBUG)
        self.stdout.write(self.style.SUCCESS('Starting Telegram bot in polling mode...'))
        scheduler.init()
        telegram_bot.polling(none_stop=True)
        self.stdout.write(self.style.SUCCESS('Telegram bot has been stopped'))
