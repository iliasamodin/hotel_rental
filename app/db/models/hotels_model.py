from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.images_model import ImagesModel


class HotelsModel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
    )
    name: Mapped[str]
    desc: Mapped[str | None]
    location: Mapped[str] = mapped_column(
        String,
        index=True,
    )
    stars: Mapped[int | None] = mapped_column(
        Integer,
        index=True,
    )
    main_image_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            ImagesModel.id,
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )

    rooms: Mapped[list["RoomsModel"]] = relationship(  # type: ignore  # noqa: F821
        "RoomsModel",
        back_populates="hotel",
    )
    image: Mapped[ImagesModel] = relationship(ImagesModel, back_populates="hotels")
    m2m_services: Mapped[list["HotelsServicesModel"]] = relationship(  # type: ignore  # noqa: F821
        "HotelsServicesModel",
        back_populates="hotel",
    )

    def __str__(self) -> str:
        return self.name
