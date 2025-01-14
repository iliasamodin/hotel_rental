from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class ResourceManagerServicePort(ABC):
    """
    Primary port of service for resource manager.
    """

    @abstractmethod
    async def get_entity_by_iid(
        self,
        entity_name: Enum,
        iid: int,
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    async def get_entities_by_filters(
        self,
        entity_name: Enum,
        filters: dict[str, str],
    ) -> list[dict[str, Any]]: ...
