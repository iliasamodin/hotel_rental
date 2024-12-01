from pathlib import Path
from types import ModuleType
from sqladmin import Admin, BaseView

from app.tools import load_modules

from app.admin_panel.utils import get_model_views


def registering_views(admin_panel: Admin) -> None:
    """
    Register views in the admin panel.
    """

    admin_panel_path = Path(__file__).resolve().parent
    modules: list[ModuleType] = load_modules(admin_panel_path)

    views: list[BaseView] = get_model_views(modules)
    for view in views:
        admin_panel.add_view(view)
