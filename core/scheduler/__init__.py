"""
Package for scheduling tasks
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from .defaults import notify_users_about_estimates


_scheduler = BackgroundScheduler()


def init():
    """
    Init the scheduler
    """
    notification_trigger = CronTrigger(hour=21, timezone='Asia/Tashkent')
    _scheduler.add_job(notify_users_about_estimates, notification_trigger)
    _scheduler.start()


def add_timer_for_comment(chat_id, rating_id: int, func):
    trigger = IntervalTrigger(minutes=5)
    _scheduler.add_job(func, trigger, [chat_id, rating_id], 
                       id='rating_{}'.format(rating_id), replace_existing=True)


def remove_timer_for_comment(rating_id: int):
    _scheduler.remove_job('rating_{}'.format(rating_id))
