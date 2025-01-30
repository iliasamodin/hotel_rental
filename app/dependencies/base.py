from fastapi import Depends

from sqlalchemy.orm import sessionmaker

from app.adapters.secondary.db.dao.transaction_context import StaticAsyncTransactionContextFactory
from app.adapters.secondary.db.session import async_session_maker


def get_async_session_maker() -> sessionmaker:
    """
    Get session-maker.

    :return: sessionmaker
    """

    return async_session_maker


def get_transaction_context_factory(
    async_session_maker: sessionmaker = Depends(get_async_session_maker),
) -> StaticAsyncTransactionContextFactory:
    """
    Get factory of transaction contexts.

    :return: transaction context factory.
    """

    transaction_context_factory = StaticAsyncTransactionContextFactory(session_maker=async_session_maker)

    return transaction_context_factory
