from sqlalchemy import ColumnCollection, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    bookings: Mapped[list["BookingsModel"]] = relationship("BookingsModel", back_populates="user")  # type: ignore

    @classmethod
    def get_columns(cls) -> ColumnCollection:
        """
        Get columns of model without password.

        :return: columns.
        """

        columns = {
            column_name: column
            for column_name, column in cls.__table__.columns.items()
            if column_name != "password"
        }

        collumn_collection = ColumnCollection(columns.items())

        return collumn_collection

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
