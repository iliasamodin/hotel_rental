from typing import Any

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    detail: str
    extras: Any = None


class BaseErrorResponseSchema(BaseResponseSchema):
    pass
