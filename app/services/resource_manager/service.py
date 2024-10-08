from typing import Any
from enum import Enum

from sqlalchemy.orm import sessionmaker

from app.dao.resource_manager.dao import ResourceManagerDAO


class ResourceManagerService:
    """
    Class of service for resource manager.
    """

    resource_manager_dao: ResourceManagerDAO

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    async def get_entity_by_iid(
        self,
        entity_name: Enum,
        iid: int,
    ) -> dict[str, Any] | None:
        """
        Get entity by iid.

        :return: entity.
        """

        async with self.session_maker.begin() as session:
            self.resource_manager_dao = ResourceManagerDAO(session=session)

            entity: dict[str, Any] | None = await self.resource_manager_dao.get_item_by_id(
                table_name=entity_name.value,
                item_id=iid,
            )

        return entity

    async def get_entities_by_filters(
        self,
        entity_name: Enum,
        filters: dict[str, str],
    ) -> list[dict[str, Any]]:
        """
        Get entities by filters.

        :return: entities.
        """

        async with self.session_maker.begin() as session:
            self.resource_manager_dao = ResourceManagerDAO(session=session)

            entity: list[dict[str, Any]] = await self.resource_manager_dao.get_items_by_filters(
                table_name=entity_name.value,
                filters=filters,
            )

        return entity
