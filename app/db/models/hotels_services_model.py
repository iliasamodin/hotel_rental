from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.hotels_model import HotelsModel
from app.db.models.service_varieties_model import ServiceVarietiesModel


class HotelsServicesModel(Base):
    __tablename__ = "hotels_services"

    hotel_id: Mapped[int] = mapped_column(
        ForeignKey(
            HotelsModel.id, 
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
        index=True,
    )
    service_variety_id: Mapped[int] = mapped_column(
        ForeignKey(
            ServiceVarietiesModel.id, 
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        primary_key=True,
        index=True,
    )
