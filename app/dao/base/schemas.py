from array import array

from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError


class OccurrenceFilterDTO[V](BaseModel):
    column_name: str
    array: array[V]

    class Config:
        arbitrary_types_allowed=True

    @field_validator("array")
    def array_validator(cls, array):
        if not array:
            raise PydanticCustomError("value_error", "value is empty array")

        return array

    @property
    def column_and_first_value(self) -> dict[str, None]:
        return {self.column_name: self.array[0]}
