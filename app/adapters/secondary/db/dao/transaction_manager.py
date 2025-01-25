from collections import defaultdict
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.ports.secondary.db.dao.base import BaseDAOPort

from app.adapters.secondary.db.dao.base.exceptions import SessionNotFoundError

from app.core.interfaces.transaction_manager import ITransactionManager


class TransactionManager(ITransactionManager):
    def __init__(
        self,
        session_maker: sessionmaker,
    ):
        self.session_maker = session_maker
        self.map_of_session_id_and_session: dict[int, AsyncSession] = {}
        self.map_of_session_id_and_daos: dict[int, list[BaseDAOPort]] = defaultdict(list)

    @asynccontextmanager
    async def __call__(
        self,
        *daos: list[BaseDAOPort],
    ) -> AsyncIterator[int]:
        """
        Assign a session to DAO instances.

        :return: session ID.
        """

        try:
            async with self.session_maker() as session:
                session_id = self._prepare_daos(daos=daos, session=session)

                yield session_id

        finally:
            await session.close()

            self._liberate_daos(session_id=session_id)

    def _prepare_daos(
        self,
        daos: list[BaseDAOPort],
        session: AsyncSession,
    ) -> int:
        """
        Assign a session to DAO instances.

        :return: session ID.
        """

        session_id = id(session)
        self.map_of_session_id_and_session[session_id] = session

        for dao in daos:
            dao.session = session
            self.map_of_session_id_and_daos[session_id].append(dao)

        return session_id

    def _liberate_daos(
        self,
        session_id: int,
    ) -> None:
        """
        Remove a session from DAO instances.
        """

        for dao in self.map_of_session_id_and_daos[session_id]:
            dao.session = None

        del self.map_of_session_id_and_daos[session_id]
        del self.map_of_session_id_and_session[session_id]

    async def commit(
        self,
        session_id: int,
    ) -> None:
        """
        Commit changes to database.
        """

        session = self.map_of_session_id_and_session.get(session_id)
        if session is None:
            raise SessionNotFoundError(
                message=f"Session id={session_id} not found.",
                extras={
                    "session_id": session_id,
                },
            )

        await session.commit()
