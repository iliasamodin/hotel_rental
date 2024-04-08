from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class HotelsModel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True,
        unique=True,
    )
    name: Mapped[str]
    location: Mapped[str] = mapped_column(
        String,
        index=True,
    )
    stars: Mapped[int | None] = mapped_column(
        Integer,
        index=True,
    )
