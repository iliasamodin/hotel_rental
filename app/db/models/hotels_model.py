from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

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
