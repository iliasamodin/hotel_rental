from typing import Annotated
from enum import Enum

from dataclasses import dataclass
from fastapi import Path


class EntityNamePathParams(Enum):
    ServiceVarieties = "service_varieties"
    Hotels = "hotels"
    PremiumLevelVarieties = "premium_level_varieties"
    Rooms = "rooms"


@dataclass
class EntityNameData:
    example = "service_varieties"
    description = "Application entity name"


entity_name_path = Path(
    example=EntityNameData.example,
    description=EntityNameData.description,
)
entity_name_annotated = Annotated[
    EntityNamePathParams,
    entity_name_path,
]
