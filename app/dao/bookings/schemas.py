from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class ServiceVarietyDTO(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None

    class Config:
        from_attributes = True


class ImageDTO(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None
    room_id: int | None = None
    filepath: str

    class Config:
        from_attributes = True


class HotelDTO(BaseModel):
    id: int
    name: str
    desc: str | None = None
    location: str
    stars: int | None = None
    main_image_id: int | None = None

    class Config:
        from_attributes = True


class ExtendedHotelDTO(HotelDTO):
    rooms_quantity: int | None = None
    main_image: ImageDTO | None = None
    services: list[ServiceVarietyDTO] | None = None


class PremiumLevelVarietyDTO(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None

    class Config:
        from_attributes = True


class RoomDTO(BaseModel):
    id: int
    name: str | None = None
    desc: str | None = None
    hotel_id: int
    premium_level_id: int | None = None
    ordinal_number: int
    maximum_persons: int
    price: float

    class Config:
        from_attributes = True


class ExtendedRoomDTO(RoomDTO):
    hotel: HotelDTO | None = None
    premium_level: PremiumLevelVarietyDTO | None = None
    services: list[ServiceVarietyDTO] | None = None


class BookingDTO(BaseModel):
    id: int
    user_id: int
    room_id: int | None
    number_of_persons: int
    check_in_dt: datetime
    check_out_dt: datetime
    total_cost: float

    class Config:
        from_attributes = True


class ExtendedBookingDTO(BookingDTO):
    room: RoomDTO | None = None
