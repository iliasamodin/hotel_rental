from string import digits, ascii_letters, punctuation

from pydantic import field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import ValidationInfo


class PhoneValidatorMixin:
    @field_validator("phone")
    def phone_validator(cls, phone: str | None) -> str | None:
        if phone is not None:
            phone = PhoneNumber._validate(phone, ValidationInfo)
            phone = phone.replace("tel:", "")

        return phone


class PasswordValidatorMixin:
    @field_validator("password")
    def password_validator(cls, password: str) -> str:
        valid_characters = set(digits + ascii_letters + punctuation)
        if not set(password).issubset(valid_characters):
            raise PydanticCustomError("value_error", "value is not a valid password")

        return password
