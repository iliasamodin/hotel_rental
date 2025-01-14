from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.secondary.db.base import Base


class ServiceVarietiesModel(Base):
    __tablename__ = "service_varieties"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
    )
    key: Mapped[str]
    name: Mapped[str | None]
    desc: Mapped[str | None]

    m2m_hotels: Mapped[list["HotelsServicesModel"]] = relationship(  # type: ignore  # noqa: F821
        "HotelsServicesModel",
        back_populates="service",
    )
    m2m_rooms: Mapped[list["RoomsServicesModel"]] = relationship(  # type: ignore  # noqa: F821
        "RoomsServicesModel",
        back_populates="service",
    )

    def __str__(self) -> str:
        return self.name
