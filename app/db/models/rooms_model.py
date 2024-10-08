from decimal import Decimal

from sqlalchemy import Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.hotels_model import HotelsModel
from app.db.models.images_model import ImagesModel
from app.db.models.premium_level_varieties_model import PremiumLevelVarietiesModel


class RoomsModel(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True,
        unique=True,
    )
    name: Mapped[str | None]
    desc: Mapped[str | None]
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey(
            HotelsModel.id, 
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        index=True,
    )
    premium_level_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            PremiumLevelVarietiesModel.id, 
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )
    ordinal_number: Mapped[int]
    maximum_persons: Mapped[int]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    main_image_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            ImagesModel.id, 
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        index=True,
    )
