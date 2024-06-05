from pydantic import BaseModel


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
