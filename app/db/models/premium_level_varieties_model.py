from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PremiumLevelVarietiesModel(Base):
    __tablename__ = "premium_level_varieties"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True,
        unique=True,
    )
    key: Mapped[str]
    name: Mapped[str | None]
    desc: Mapped[str | None]
