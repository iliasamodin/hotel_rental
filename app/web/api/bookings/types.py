from typing import Annotated

from dataclasses import dataclass
from fastapi import Query


@dataclass
class HotelStarsData:
    example = 5
    ge = 1
    le = 6
    description = "Number of stars for hotels"


@dataclass
class ServiceIdsData:
    example = [1, 2]
    description = "List of services"


@dataclass
class PremiumLevelIdsData:
    example = [1, 2]
    description = "List of premium Levels"


hotel_stars_query = Query(
    example=HotelStarsData.example,
    ge=HotelStarsData.ge,
    le=HotelStarsData.le,
    description=HotelStarsData.description,
)
hotel_stars_annotated = Annotated[
    int,
    hotel_stars_query,
]

service_ids_query = Query(
    example=ServiceIdsData.example,
    description=ServiceIdsData.description,
)
service_ids_annotated = Annotated[
    list[int],
    service_ids_query,
]

premium_level_ids_query = Query(
    example=PremiumLevelIdsData.example,
    description=PremiumLevelIdsData.description,
)
premium_level_ids_annotated = Annotated[
    list[int],
    premium_level_ids_query,
]
