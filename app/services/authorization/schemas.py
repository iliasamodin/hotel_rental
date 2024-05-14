from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.services.base.mixins import PhoneValidatorMixin, PasswordValidatorMixin


class BaseUserSchema(BaseModel, PhoneValidatorMixin):
    email: EmailStr
    phone: str
    first_name: str
    last_name: str


class UserRequestSchema(BaseUserSchema, PasswordValidatorMixin):
    password: str


class UserResponseSchema(BaseUserSchema):
    id: int


class TokenResponseSchema(BaseModel):
    token: str
    expires: datetime
