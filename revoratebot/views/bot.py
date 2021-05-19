from django.views import View
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from telebot.types import Update
from Revorate.settings import WEBHOOK_URL_PATH, WEBHOOK_URL_BASE, WEBHOOK_SSL_CERT


class BotInitializeView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        from bot import telegram_bot
        telegram_bot.remove_webhook()
        telegram_bot.set_webhook(WEBHOOK_URL_BASE + '/' + WEBHOOK_URL_PATH, certificate=open(WEBHOOK_SSL_CERT, 'r'))
        from core import scheduler
        scheduler.init()
        return HttpResponse('Initialized Successfully!')


@method_decorator(csrf_exempt, name='dispatch')
class BotUpdatesRecieverView(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.content_type != 'application/json':
            return HttpResponseBadRequest()
        json_string = request.body.decode('utf-8')
        update = Update.de_json(json_string)
        from bot import telegram_bot
        telegram_bot.process_new_updates([update])
        return HttpResponse('')
