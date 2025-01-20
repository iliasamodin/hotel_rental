from fastapi import Depends

from app.adapters.secondary.db.dao.authorization.dao import AuthorizationDAO
from app.adapters.secondary.db.dao.transaction_manager import TransactionManager

from app.core.services.authorization.service import AuthorizationService

from app.dependencies.base import get_transaction_manager


def get_authorization_dao() -> AuthorizationDAO:
    """
    Get authorization DAO.

    :return: authorization DAO.
    """

    dao = AuthorizationDAO()

    return dao


def get_authorization_service(
    transaction_manager: TransactionManager = Depends(get_transaction_manager),
    authorization_dao: AuthorizationDAO = Depends(get_authorization_dao),
) -> AuthorizationService:
    """
    Get authorization service.

    :return: authorization service.
    """

    service = AuthorizationService(
        transaction_manager=transaction_manager,
        authorization_dao=authorization_dao,
    )

    return service
