from pydantic import BaseModel


class ServiceVarietyResponseSchema(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None


class ListOfServicesRequestSchema(BaseModel):
    service_ids: list[int]


class HotelSchema(BaseModel):
    id: int
    name: str
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
