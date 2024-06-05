from enum import Enum

from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedRoomResponseSchema,
    HotelSchema,
)

from app.web.api.base.schemas import BaseErrorResponseSchema


class ServicesEnum(Enum):
    """
    Scheme of responses to a request for a selection of services.
    """

    SUCCESS: ServiceVarietyResponseSchema = ServiceVarietyResponseSchema(
        id=1,
        key="wifi",
        name="Free Wi-Fi",
        desc="Free Wi-Fi.",
    )
    CONSISTENCY_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Service filters for hotels only or rooms only are mutually exclusive.",
        extras={
            "only_for_hotels": True,
            "only_for_rooms": True,
        },
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation.",
        },
    )


class HotelsEnum(Enum):
    """
    Scheme of responses to a request for a selection of hotels.
    """

    SUCCESS: ExtendedHotelResponseSchema = ExtendedHotelResponseSchema(
        id=1,
        name="Cosmos Collection Altay Resort",
        desc="Colorful description for hotel #1",
        location="Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
        stars=3,
        rooms_quantity=50,
        services=[
            ServiceVarietyResponseSchema(
                id=1,
                key="wifi",
                name="Free Wi-Fi",
                desc="Free Wi-Fi.",
            ),
        ],
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation.",
        },
    )


class PremiumLevelsEnum(Enum):
    """
    Scheme of responses to a request for a selection of premium levels.
    """

    SUCCESS: PremiumLevelVarietyResponseSchema = PremiumLevelVarietyResponseSchema(
        id=1,
        key="budget",
        name="Budget service",
        desc="Minimum service for the level of the hotel to which the room belongs.",
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation.",
        },
    )


class RoomsEnum(Enum):
    """
    Scheme of responses to a request for a selection of rooms.
    """

    SUCCESS: ExtendedRoomResponseSchema = ExtendedRoomResponseSchema(
        id=1,
        name="Room #1 of hotel #1",
        desc="Colorful description for room #1 of hotel #1.",
        hotel_id=1,
        premium_level_id=1,
        ordinal_number=1,
        maximum_persons=1,
        price=24_500,
        hotel=HotelSchema(
            id=1,
            name="Cosmos Collection Altay Resort",
            desc="Colorful description for hotel #1",
            location="Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
            stars=3,
        ),
        premium_level=PremiumLevelVarietyResponseSchema(
            id=1,
            key="budget",
            name="Budget service",
            desc="Minimum service for the level of the hotel to which the room belongs.",
        ),
        services=[
            ServiceVarietyResponseSchema(
                id=1,
                key="wifi",
                name="Free Wi-Fi",
                desc="Free Wi-Fi.",
            ),
        ],
    )
    CONSISTENCY_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="The minimum room price filter must be less than the maximum room price filter.",
        extras={
            "min_price": 100_000,
            "max_price": 35_000,
        },
    )
    SERVER_ERR: BaseErrorResponseSchema = BaseErrorResponseSchema(
        detail="Unspecified error.",
        extras={
            "doc": "Exception documentation.",
        },
    )
