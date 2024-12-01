from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

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

    hotel: Mapped[HotelsModel] = relationship(HotelsModel, back_populates="m2m_services")
    service: Mapped[ServiceVarietiesModel] = relationship(ServiceVarietiesModel, back_populates="m2m_hotels")

    def __str__(self) -> str:
        return f"M2M relation for hotel {self.hotel_id} and service {self.service_variety_id}"
