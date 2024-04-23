from pydantic import BaseModel


class ServiceVarietyDTO(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None

    class Config:
        from_attributes = True


class HotelDTO(BaseModel):
    id: int
    name: str
    location: str
    stars: int | None = None

    class Config:
        from_attributes = True


class ExtendedHotelDTO(HotelDTO):
    rooms_quantity: int | None = None
    services: list[ServiceVarietyDTO] | None = None
