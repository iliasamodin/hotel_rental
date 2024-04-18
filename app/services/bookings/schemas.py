from pydantic import BaseModel


class ServiceVarietyResponseSchema(BaseModel):
    id: int
    key: str
    name: str | None = None
    desc: str | None = None
