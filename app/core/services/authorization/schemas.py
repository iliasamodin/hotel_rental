from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.core.services.base.mixins import PhoneValidatorMixin, PasswordValidatorMixin


class BaseUserSchema(BaseModel, PhoneValidatorMixin):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str


class UserRequestSchema(BaseUserSchema, PasswordValidatorMixin):
    password: str


class UserResponseSchema(BaseUserSchema):
    id: int
    is_admin: bool = False


class TokenResponseSchema(BaseModel):
    token: str
    expires: datetime
