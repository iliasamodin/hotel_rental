from sqlalchemy import Integer, ForeignKey, select, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

from app.settings import settings

from app.db.base import Base


class ImagesModel(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True,
        unique=True,
    )
    key: Mapped[str]
    name: Mapped[str | None]
    desc: Mapped[str | None]
    room_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            f"{Base.metadata.schema}.rooms.id", 
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )

    @hybrid_property
    def filepath(self):
        return f"{settings.PATH_OF_BOOKING_IMAGES}/{self.key}"

    @filepath.expression
    def filepath(cls):
        return func.concat(
            settings.PATH_OF_BOOKING_IMAGES,
            "/",
            cls.key,
        ).label("filepath")
