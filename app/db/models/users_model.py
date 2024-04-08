from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
    )
    phone: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
    )
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(
        String,
        index=True,
    )
