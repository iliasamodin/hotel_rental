from abc import ABC, abstractmethod
from typing import AsyncIterator

from app.ports.secondary.db.dao.base import BaseDAOPort


class ITransactionManager(ABC):
    @abstractmethod
    async def __call__(
        self,
        *daos: list[BaseDAOPort],
    ) -> AsyncIterator[int]: ...

    @abstractmethod
    def prepare_daos(
        self,
        daos: list[BaseDAOPort],
        session,
    ) -> int: ...

    @abstractmethod
    def liberate_daos(
        self,
        session_id: int,
    ) -> None: ...

    @abstractmethod
    async def commit(
        self,
        session_id: int,
    ) -> None: ...
