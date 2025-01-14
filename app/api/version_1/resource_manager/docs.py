from enum import Enum

from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    HotelSchema,
    PremiumLevelVarietyResponseSchema,
    RoomSchema,
)

from app.api.base.schemas import BaseErrorResponseSchema


class GettingEntityEnum(Enum):
    """
    Scheme of responses to a request for a selection of entity by iid.
    """

    SUCCESS_FOR_SERVICE: ServiceVarietyResponseSchema = ServiceVarietyResponseSchema(
        id=1,
        key="wifi",
        name="Free Wi-Fi",
        desc="Free Wi-Fi.",
    )
    SUCCESS_FOR_HOTEL: HotelSchema = HotelSchema(
        id=1,
        name="Cosmos Collection Altay Resort",
        desc="Colorful description for hotel #1.",
        location="Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
        stars=3,
    )
    SUCCESS_FOR_PREMIUM_LEVEL: PremiumLevelVarietyResponseSchema = PremiumLevelVarietyResponseSchema(
        id=1,
        key="budget",
        name="Budget service",
        desc="Minimum service for the level of the hotel to which the room belongs.",
    )
    SUCCESS_FOR_ROOM: RoomSchema = RoomSchema(
        id=1,
        name="Room #1 of hotel #1",
        desc="Colorful description for room #1 of hotel #1.",
        hotel_id=1,
        premium_level_id=1,
        ordinal_number=1,
        maximum_persons=1,
        price=24_500,
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation.",
        },
    )
