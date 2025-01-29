from fastapi import Depends

from app.adapters.secondary.db.dao.authorization.dao import AuthorizationDAO
from app.adapters.secondary.db.dao.transaction_context import StaticAsyncTransactionContextFactory

from app.core.services.authorization.service import AuthorizationService

from app.dependencies.base import get_transaction_context_factory


def get_authorization_dao() -> AuthorizationDAO:
    """
    Get authorization DAO.

    :return: authorization DAO.
    """

    dao = AuthorizationDAO()

    return dao


def get_authorization_service(
    transaction_context_factory: StaticAsyncTransactionContextFactory = Depends(get_transaction_context_factory),
    authorization_dao: AuthorizationDAO = Depends(get_authorization_dao),
) -> AuthorizationService:
    """
    Get authorization service.

    :return: authorization service.
    """

    service = AuthorizationService(
        transaction_context_factory=transaction_context_factory,
        authorization_dao=authorization_dao,
    )

    return service
