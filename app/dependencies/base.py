from fastapi import Depends
from sqlalchemy.orm import sessionmaker

from app.adapters.secondary.db.session import async_session_maker

from app.adapters.secondary.db.dao.transaction_manager import TransactionManager


def get_async_session_maker() -> sessionmaker:
    """
    Get session-maker.

    :return: sessionmaker
    """

    return async_session_maker


def get_transaction_manager(
    async_session_maker: sessionmaker = Depends(get_async_session_maker),
) -> TransactionManager:
    """
    Get transaction manager.

    :return: transaction manager.
    """

    transaction_manager = TransactionManager(session_maker=async_session_maker)

    return transaction_manager
