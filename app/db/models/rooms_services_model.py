from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.rooms_model import RoomsModel
from app.db.models.service_varieties_model import ServiceVarietiesModel


class RoomsServicesModel(Base):
    __tablename__ = "rooms_services"

    room_id: Mapped[int] = mapped_column(
        ForeignKey(
            RoomsModel.id, 
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
