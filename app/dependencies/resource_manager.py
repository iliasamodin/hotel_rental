from fastapi import Depends

from app.adapters.secondary.db.dao.resource_manager.dao import ResourceManagerDAO
from app.adapters.secondary.db.dao.transaction_context import StaticAsyncTransactionContextFactory

from app.core.services.resource_manager.service import ResourceManagerService

from app.dependencies.base import get_transaction_context_factory


def get_resource_manager_dao() -> ResourceManagerDAO:
    """
    Get resource manager DAO.

    :return: resource manager DAO.
    """

    dao = ResourceManagerDAO()

    return dao


def get_resource_manager_service(
    transaction_context_factory: StaticAsyncTransactionContextFactory = Depends(get_transaction_context_factory),
    resource_manager_dao: ResourceManagerDAO = Depends(get_resource_manager_dao),
) -> ResourceManagerService:
    """
    Get resource manager service.

    :return: resource manager service.
    """

    service = ResourceManagerService(
        transaction_context_factory=transaction_context_factory,
        resource_manager_dao=resource_manager_dao,
    )

    return service
