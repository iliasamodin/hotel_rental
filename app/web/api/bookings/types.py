from typing import Annotated

from dataclasses import dataclass
from fastapi import Query


@dataclass
class HotelStarsData:
    example = 5
    ge = 1
    le = 6
    description = "Number of stars for hotels"


hotel_stars_query = Query(
    examples=HotelStarsData.example,
    ge=HotelStarsData.ge,
    le=HotelStarsData.le,
    description=HotelStarsData.description,
)
hotel_stars_annotated = Annotated[
    int,
    hotel_stars_query,
]
