from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


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
