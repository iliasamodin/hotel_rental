from celery import Celery

from app.settings import settings


celery_app = Celery(
    main="celery_app",
    broker=settings.REDIS_URL,
    include=["app.celery.tasks"],
)
