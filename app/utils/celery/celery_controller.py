from celery import Celery
from sqlalchemy.orm import sessionmaker

from app.settings import settings

from app.adapters.secondary.db.session import sync_session_maker

from app.utils.celery.celery_app import celery_app
from app.utils.celery.fake_task import FakeTask


class CeleryController:
    """
    Celery task queue controller.
    """

    def __init__(
        self,
        celery_app: Celery = celery_app,
        session_maker: sessionmaker = sync_session_maker,
        fake_task: FakeTask = FakeTask,
    ):
        self.celery_app = celery_app
        self.session_maker = session_maker
        self.fake_task = fake_task

    def task(self, *args, **opts):
        """
        Determine whether a task can be executed in a task queue.
        """

        if settings.NEED_TO_SENDING_EMAIL and settings.MODE != "test":
            return self.celery_app.task(*args, **opts)

        return self.fake_task()


celery_controller = CeleryController()
