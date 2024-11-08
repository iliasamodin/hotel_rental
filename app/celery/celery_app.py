from celery import Celery
from celery.schedules import crontab

from app.settings import settings


celery_app = Celery(
    main="celery_app",
    broker=settings.REDIS_URL,
    include=[
        "app.celery.tasks",
        "app.celery.scheduled",
    ],
)

# Declaring cron configurations of celery application
#   to perform regular tasks
celery_app.conf.beat_schedule = {
    "booking_reminders": {
        "task": "booking_reminders",
        "schedule": crontab(
            hour=str(settings.CHECK_IN_TIME),
            minute="0",
        ),
    },
}
