from types import ModuleType

from sqladmin import BaseView
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


def get_model_views(modules: list[ModuleType]) -> list[BaseView]:
    """
    Get all views from modules.

    :return: list of views.
    """

    views: list[BaseView] = []
    for module in modules:
        for view in module.__dict__.values():
            if all(
                (
                    getattr(view, "is_view", False),
                    getattr(view, "is_visible", False),
                    getattr(view, "is_accessible", False),
                ),
            ):
                views.append(view)

    return views


def get_model_view_name(model: DeclarativeAttributeIntercept) -> str:
    """
    Get model view name.

    :return: name of model view.
    """

    name = model.__tablename__.replace("_", " ").capitalize()

    return name
