from celery import Celery

from app.settings import settings

from app.celery.celery_app import celery_app
from app.celery.fake_tasks import FakeTask


class CeleryController:
    """
    Celery task queue controller.
    """

    def __init__(
        self,
        celery_app: Celery = celery_app,
    ):
        self.celery_app = celery_app

    def task(self, *args, **opts):
        """
        Determine whether a task can be executed in a task queue.
        """

        if settings.SENDING_EMAIL and settings.MODE != "test":
            return self.celery_app.task(*args, **opts)

        return FakeTask()


celery_controller = CeleryController()
