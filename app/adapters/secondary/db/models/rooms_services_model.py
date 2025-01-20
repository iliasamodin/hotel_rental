from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.secondary.db.base import Base
from app.adapters.secondary.db.models.rooms_model import RoomsModel
from app.adapters.secondary.db.models.service_varieties_model import ServiceVarietiesModel


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

    room: Mapped[RoomsModel] = relationship(RoomsModel, back_populates="m2m_services")
    service: Mapped[ServiceVarietiesModel] = relationship(ServiceVarietiesModel, back_populates="m2m_rooms")

    def __str__(self) -> str:
        return f"M2M relation for room {self.room_id} and service {self.service_variety_id}"
