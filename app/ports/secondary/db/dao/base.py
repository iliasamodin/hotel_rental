from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.core.services.base.dtos import OccurrenceFilterDTO


class BaseDAOPort(ABC):
    """
    DAO layer base secondary port.
    """

    @abstractmethod
    def _get_model_by_table_name(self, table_name: str) -> DeclarativeAttributeIntercept: ...

    @abstractmethod
    async def get_item_by_id(
        self,
        table_name: str,
        item_id: int,
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    async def get_items_by_filters(
        self,
        table_name: str,
        filters: dict[str, Any] | None = None,
        occurrence: OccurrenceFilterDTO | None = None,
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def insert_item(
        self,
        table_name: str,
        item_data: dict[str, Any] | BaseModel,
    ) -> None: ...

    @abstractmethod
    async def delete_item_by_id(
        self,
        table_name: str,
        item_id: int,
    ) -> dict[str, Any]: ...
