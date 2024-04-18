from pydantic import BaseModel


class ServiceVarietyDTO(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None

    class Config:
        from_attributes=True
