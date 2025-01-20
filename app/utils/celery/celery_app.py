from celery import Celery
from celery.schedules import crontab

from app.settings import settings


celery_app = Celery(
    main="celery_app",
    broker=settings.REDIS_URL,
    include=[
        "app.utils.celery.tasks",
        "app.utils.celery.scheduled",
    ],
)

beat_schedule = {}
if settings.NEED_TO_SENDING_EMAIL:
    beat_schedule["booking_reminders"] = {
        "task": "booking_reminders",
        "schedule": crontab(
            hour=str(settings.CHECK_IN_TIME),
            minute="0",
        ),
    }
if settings.NEED_TO_WARM_UP_CACHE:
    beat_schedule["warm_up_cache"] = {
        "task": "warm_up_cache",
        "schedule": settings.WARM_UP_CACHE_SECONDS,
    }

# Declaring cron configurations of celery application
#   to perform regular tasks
celery_app.conf.beat_schedule = beat_schedule
