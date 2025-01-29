from typing import Any
from enum import Enum

from app.ports.primary.resource_manager import ResourceManagerServicePort
from app.ports.secondary.db.dao.resource_manager import ResourceManagerDAOPort

from app.core.interfaces.transaction_context import IStaticAsyncTransactionContextFactory
from app.core.services.resource_manager.exceptions import EntityNotExistsError


class ResourceManagerService(ResourceManagerServicePort):
    """
    Class of service for resource manager.
    """

    def __init__(
        self,
        transaction_context_factory: IStaticAsyncTransactionContextFactory,
        resource_manager_dao: ResourceManagerDAOPort,
    ):
        self.transaction_context_factory = transaction_context_factory
        self.resource_manager_dao = resource_manager_dao

    async def get_entity_by_iid(
        self,
        entity_name: Enum,
        iid: int,
    ) -> dict[str, Any]:
        """
        Get entity by iid.

        :return: entity.
        """

        transaction_context = self.transaction_context_factory.init_transaction_context()
        async with transaction_context():
            entity: dict[str, Any] | None = await self.resource_manager_dao.get_item_by_id(
                transaction_context=transaction_context,
                table_name=entity_name.value,
                item_id=iid,
            )

            if entity is None:
                raise EntityNotExistsError(
                    message=f"Entity with id={iid} not found.",
                    extras={
                        "entity_name": entity_name.value,
                        "iid": iid,
                    },
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

        transaction_context = self.transaction_context_factory.init_transaction_context()
        async with transaction_context():
            entity: list[dict[str, Any]] = await self.resource_manager_dao.get_items_by_filters(
                transaction_context=transaction_context,
                table_name=entity_name.value,
                filters=filters,
            )

        return entity
