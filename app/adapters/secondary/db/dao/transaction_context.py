from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from typing import Any

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.adapters.secondary.db.dao.base.exceptions import (
    TransactionContextAttrAlreadySetError,
    TransactionContextAttrNotSetError,
)

from app.core.interfaces.transaction_context import (
    IStaticAsyncTransactionContext,
    IStaticAsyncTransactionContextFactory,
    IStaticSyncTransactionContext,
    IStaticSyncTransactionContextFactory,
)


class StaticSyncTransactionContext(IStaticSyncTransactionContext):
    """
    The context of the database sync connection
    for transactional execution of queries.
    """

    def __init__(
        self,
        session_maker: sessionmaker,
    ):
        self._session_maker: sessionmaker = session_maker
        self._session: AsyncSession | None = None

    def __getattr__(self, name: str) -> Any:
        return getattr(self.session, name)

    @contextmanager
    def __call__(
        self,
        reraise: Exception | None = None,
        skip: tuple[Exception] | Exception | None = None,
    ) -> Iterator["StaticSyncTransactionContext"]:
        """
        Determine the connect to the database.

        :return: transaction context.
        """

        if self._session is not None:
            raise TransactionContextAttrAlreadySetError("Session is already initialized.")

        try:
            with self.session_maker() as session:
                try:
                    self._session = session

                    yield self

                finally:
                    self.close()

        except Exception as error:
            logger.error(error)

            if reraise and (not skip or (skip and not isinstance(error, skip))):
                raise reraise
            raise

    @property
    def session_maker(self) -> sessionmaker:
        return self._session_maker

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise TransactionContextAttrNotSetError("Session is not initialized.")

        return self._session

    def commit(self) -> None:
        """
        Commit the transaction.
        """

        self.session.commit()

    def close(self) -> None:
        """
        Close the transaction.
        """

        try:
            current_session = self.session
            self._session = None

            current_session.close()

        except Exception as error:
            logger.error(error)


class StaticSyncTransactionContextFactory(IStaticSyncTransactionContextFactory):
    """
    Factory of sync transaction contexts.
    """

    def __init__(
        self,
        session_maker: sessionmaker,
    ):
        self.session_maker = session_maker

    def init_transaction_context(self) -> StaticSyncTransactionContext:
        transaction_context = StaticSyncTransactionContext(session_maker=self.session_maker)

        return transaction_context


class StaticAsyncTransactionContext(IStaticAsyncTransactionContext):
    """
    The context of the database async connection
    for transactional execution of queries.
    """

    def __init__(
        self,
        session_maker: sessionmaker,
    ):
        self._session_maker: sessionmaker = session_maker
        self._session: AsyncSession | None = None

    def __getattr__(self, name: str) -> Any:
        return getattr(self.session, name)

    @asynccontextmanager
    async def __call__(
        self,
        reraise: Exception | None = None,
        skip: tuple[Exception] | Exception | None = None,
    ) -> AsyncIterator["StaticAsyncTransactionContext"]:
        """
        Determine the connect to the database.

        :return: transaction context.
        """

        if self._session is not None:
            raise TransactionContextAttrAlreadySetError("Session is already initialized.")

        try:
            async with self.session_maker() as session:
                try:
                    self._session = session

                    yield self

                finally:
                    await self.close()

        except Exception as error:
            logger.error(error)

            if reraise and (not skip or (skip and not isinstance(error, skip))):
                raise reraise
            raise

    @property
    def session_maker(self) -> sessionmaker:
        return self._session_maker

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise TransactionContextAttrNotSetError("Session is not initialized.")

        return self._session

    async def commit(self) -> None:
        """
        Commit the transaction.
        """

        await self.session.commit()

    async def close(self) -> None:
        """
        Close the transaction.
        """

        try:
            current_session = self.session
            self._session = None

            await current_session.close()

        except Exception as error:
            logger.error(error)


class StaticAsyncTransactionContextFactory(IStaticAsyncTransactionContextFactory):
    """
    Factory of async transaction contexts.
    """

    def __init__(
        self,
        session_maker: sessionmaker,
    ):
        self.session_maker = session_maker

    def init_transaction_context(self) -> StaticAsyncTransactionContext:
        transaction_context = StaticAsyncTransactionContext(session_maker=self.session_maker)

        return transaction_context
