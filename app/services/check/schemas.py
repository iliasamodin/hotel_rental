from pydantic import BaseModel, model_validator

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
