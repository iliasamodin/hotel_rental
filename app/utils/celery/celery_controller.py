from celery import Celery

from app.settings import settings

from app.adapters.secondary.db.session import sync_session_maker
from app.adapters.secondary.db.dao.transaction_context import StaticSyncTransactionContextFactory

from app.core.interfaces.transaction_context import IStaticSyncTransactionContextFactory

from app.utils.celery.celery_app import celery_app
from app.utils.celery.fake_task import FakeTask, fake_task

transaction_context_factory = StaticSyncTransactionContextFactory(session_maker=sync_session_maker)


class CeleryController:
    """
    Celery task queue controller.
    """

    def __init__(
        self,
        celery_app: Celery = celery_app,
        transaction_context_factory: IStaticSyncTransactionContextFactory = transaction_context_factory,
        fake_task: FakeTask = fake_task,
    ):
        self.celery_app = celery_app
        self.transaction_context_factory = transaction_context_factory
        self.fake_task = fake_task

    def task(self, *args, **opts):
        """
        Determine whether a task can be executed in a task queue.
        """

        if settings.NEED_TO_SENDING_EMAIL and settings.MODE != "test":
            return self.celery_app.task(*args, **opts)

        return self.fake_task


celery_controller = CeleryController()
