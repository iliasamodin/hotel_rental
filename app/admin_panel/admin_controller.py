from pathlib import Path
from types import ModuleType
from fastapi import FastAPI
from sqladmin import Admin, BaseView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine

from app.settings import settings

from app.db.session import async_engine

from app.tools import load_modules

from app.admin_panel.utils import get_model_views
from app.admin_panel.auth import authentication_backend


class AdminPanelController:
    def __init__(
        self,
    ):
        self.app: FastAPI | None = None
        self.admin_panel: Admin | None = None

    def registering_app_to_controller(self, app: FastAPI) -> None:
        """
        Registering app to admin panel controller.
        """

        self.app = app

    def registering_views(
        self,
        engine: Engine | AsyncEngine = async_engine,
        authentication_backend: AuthenticationBackend = authentication_backend,
    ) -> None:
        """
        Registering views in the admin panel.
        """

        self.admin_panel = Admin(
            app=self.app,
            engine=engine,
            base_url=settings.ADMIN_PANEL_BASE_URL,
            authentication_backend=authentication_backend,
        )

        admin_panel_path = Path(__file__).resolve().parent
        modules: list[ModuleType] = load_modules(path=admin_panel_path)

        views: list[BaseView] = get_model_views(modules=modules)
        for view in views:
            self.admin_panel.add_view(view)


admin_panel_controller = AdminPanelController()
