from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.users_model import UsersModel
from app.db.models.rooms_model import RoomsModel


class BookingsModel(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            UsersModel.id, 
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )
    room_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            RoomsModel.id, 
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )
    number_of_persons: Mapped[int]
    check_in_dt: Mapped[datetime]
    check_out_dt: Mapped[datetime]
    total_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    user: Mapped[UsersModel] = relationship(UsersModel, back_populates="bookings")
    room: Mapped[RoomsModel] = relationship(RoomsModel, back_populates="bookings")

    def __str__(self) -> str:
        return f"Check in from {self.check_in_dt.strftime("%Y-%m-%d %H:%M:%S %Z")}"
