from sqladmin import ModelView

from app.adapters.secondary.db.models.bookings_model import BookingsModel
from app.adapters.secondary.db.models.hotels_model import HotelsModel
from app.adapters.secondary.db.models.hotels_services_model import HotelsServicesModel
from app.adapters.secondary.db.models.images_model import ImagesModel
from app.adapters.secondary.db.models.premium_level_varieties_model import PremiumLevelVarietiesModel
from app.adapters.secondary.db.models.rooms_model import RoomsModel
from app.adapters.secondary.db.models.rooms_services_model import RoomsServicesModel
from app.adapters.secondary.db.models.service_varieties_model import ServiceVarietiesModel
from app.adapters.secondary.db.models.users_model import UsersModel

from app.utils.admin_panel.base import BaseCustomModelView


class BookingsModelView(
    ModelView,
    BaseCustomModelView,
    model=BookingsModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class HotelsModelView(
    ModelView,
    BaseCustomModelView,
    model=HotelsModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class HotelsServicesModelView(
    ModelView,
    BaseCustomModelView,
    model=HotelsServicesModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class ImagesModelView(
    ModelView,
    BaseCustomModelView,
    model=ImagesModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class PremiumLevelVarietiesModelView(
    ModelView,
    BaseCustomModelView,
    model=PremiumLevelVarietiesModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class RoomsModelView(
    ModelView,
    BaseCustomModelView,
    model=RoomsModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class RoomsServicesModelView(
    ModelView,
    BaseCustomModelView,
    model=RoomsServicesModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class ServiceVarietiesModelView(
    ModelView,
    BaseCustomModelView,
    model=ServiceVarietiesModel,
):
    name_plural = BaseCustomModelView.name_plural

    column_list = BaseCustomModelView.model_columns
    column_details_list = "__all__"
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns


class UsersModelView(
    ModelView,
    BaseCustomModelView,
    model=UsersModel,
):
    name_plural = BaseCustomModelView.name_plural

    can_delete = False
    column_list = BaseCustomModelView.model_columns
    column_details_exclude_list = [UsersModel.password]
    column_export_list = BaseCustomModelView.model_columns
    form_columns = BaseCustomModelView.model_columns
