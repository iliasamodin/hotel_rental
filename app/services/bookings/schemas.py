from datetime import date, datetime

from pydantic import BaseModel

from app.services.check.schemas import CheckInAndCheckOutValidator


class ServiceVarietyResponseSchema(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None


class HotelSchema(BaseModel):
    id: int
    name: str
    desc: str | None = None
    location: str
    stars: int | None = None


class ExtendedHotelResponseSchema(HotelSchema):
    rooms_quantity: int | None = None
    services: list[ServiceVarietyResponseSchema]


class PremiumLevelVarietyResponseSchema(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None


class RoomSchema(BaseModel):
    id: int
    name: str | None = None
    desc: str | None = None
    hotel_id: int
    premium_level_id: int | None = None
    ordinal_number: int
    maximum_persons: int
    price: float


class ExtendedRoomResponseSchema(RoomSchema):
    hotel: HotelSchema | None = None
    premium_level: PremiumLevelVarietyResponseSchema | None = None
    services: list[ServiceVarietyResponseSchema]


class BaseBookingSchema(BaseModel):
    user_id: int
    room_id: int | None
    number_of_persons: int
    check_in_dt: datetime
    check_out_dt: datetime
    total_cost: float


class BookingResponseSchema(BaseBookingSchema):
    id: int


class ExtendedBookingResponseSchema(BookingResponseSchema):
    room: RoomSchema | None = None


class BookingRequestSchema(CheckInAndCheckOutValidator):
    room_id: int
    number_of_persons: int
