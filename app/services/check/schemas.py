from datetime import date, datetime, timedelta

from pydantic import BaseModel, model_validator, EmailStr

from app.settings import settings

from app.services.base.mixins import PhoneValidatorMixin, PasswordValidatorMixin
from app.services.check.exceptions import DataValidationError


class HotelsOrRoomsValidator(BaseModel):
    only_for_hotels: bool = False
    only_for_rooms: bool = False

    @model_validator(mode="after")
    def consistency_of_mutually_exclusive_boolean_values_validator(self) -> "HotelsOrRoomsValidator":
        """
        Check that mutually exclusive boolean values
        are consistent with each other.

        :return: scheme for limiting service query.
        :raise: DataValidationError
        """

        if self.only_for_hotels and self.only_for_rooms:
            raise DataValidationError(
                message="Service filters for hotels only or rooms only are mutually exclusive.",
                extras={
                    "only_for_hotels": self.only_for_hotels,
                    "only_for_rooms": self.only_for_rooms,
                },
            )

        return self


class PriceRangeValidator(BaseModel):
    min_price: float | None = None
    max_price: float | None = None

    @model_validator(mode="after")
    def price_boundary_consistency_validator(self) -> "PriceRangeValidator":
        """
        Check the consistency of price limits relative to each other.

        :return: scheme for limiting room query.
        :raise: DataValidationError
        """

        if self.min_price is not None and self.max_price is not None and self.min_price > self.max_price:
            raise DataValidationError(
                message="The minimum room price filter must be less than the maximum room price filter.",
                extras={
                    "min_price": self.min_price,
                    "max_price": self.max_price,
                },
            )

        return self


class UserAuthenticationValidator(BaseModel, PhoneValidatorMixin, PasswordValidatorMixin):
    email: EmailStr | None = None
    phone: str | None = None
    password: str

    @model_validator(mode="after")
    def email_or_phone_validator(self) -> "UserAuthenticationValidator":
        """
        Check if there is a value for email or phone.

        :return: scheme for authentication.
        :raise: DataValidationError
        """

        if self.email is None and self.phone is None:
            raise DataValidationError(
                message="To identify the user, you need to pass the email or phone value.",
                extras={
                    "email": self.email,
                    "phone": self.phone,
                },
            )

        return self


class MinAndMaxDtsValidator(BaseModel):
    min_dt: datetime | None
    max_dt: datetime | None

    @model_validator(mode="after")
    def time_range_validator(self) -> "MinAndMaxDtsValidator":
        """
        Check min and max dates for consistency.

        return: Schema of min and max dates.
        raise: DataValidationError
        """

        if (
            self.min_dt is not None
            and self.max_dt is not None
            and self.min_dt + timedelta(hours=settings.MIN_RENTAL_INTERVAL_HOURS) > self.max_dt
        ):
            raise DataValidationError(
                message=f"The maximum date must be at least {settings.MIN_RENTAL_INTERVAL_HOURS} hours later "
                "than the minimum.",
                extras={
                    "min_dt": self.min_dt.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "max_dt": self.max_dt.strftime("%Y-%m-%dT%H:%M:%S%z"),
                },
            )

        return self


class CheckInAndCheckOutValidator(BaseModel):
    check_in_date: date
    check_out_date: date

    @model_validator(mode="after")
    def date_range_validator(self) -> "CheckInAndCheckOutValidator":
        """
        Check the consistency of the check-in and check-out dates.

        return: Schema of check-in and check-out dates.
        raise: DataValidationError
        """

        if self.check_in_date is not None and self.check_out_date is not None:
            if self.check_in_date >= self.check_out_date:
                raise DataValidationError(
                    message="Check-out date must be later than check-in date.",
                    extras={
                        "check_in_date": self.check_in_date.strftime("%Y-%m-%d"),
                        "check_out_date": self.check_out_date.strftime("%Y-%m-%d"),
                    },
                )

            elif (self.check_out_date - self.check_in_date).days > settings.MAX_RENTAL_INTERVAL_DAYS:
                raise DataValidationError(
                    message=f"The maximum rental period is {settings.MAX_RENTAL_INTERVAL_DAYS} days.",
                    extras={
                        "check_in_date": self.check_in_date.strftime("%Y-%m-%d"),
                        "check_out_date": self.check_out_date.strftime("%Y-%m-%d"),
                    },
                )

        return self
