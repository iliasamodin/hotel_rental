from typing import ClassVar

from sqlalchemy import ColumnCollection

from app.admin_panel.utils import get_model_view_name


class BaseCustomView:
    is_view = True


class BaseCustomModelView(BaseCustomView):
    model: ClassVar[type]

    @property
    def name_plural(self) -> str:
        return get_model_view_name(model=self.model)

    @property
    def model_columns(self) -> ColumnCollection:
        return self.model.get_columns()
