from abc import ABC, abstractmethod
from collections.abc import AsyncIterator, Iterator


class IStaticSyncTransactionContext(ABC):
    @abstractmethod
    def __call__(self) -> Iterator[None]: ...

    @abstractmethod
    def session_maker(self): ...

    @abstractmethod
    def session(self): ...

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def close(self) -> None: ...


class IStaticSyncTransactionContextFactory(ABC):
    @abstractmethod
    def init_transaction_context(self) -> IStaticSyncTransactionContext: ...


class IStaticAsyncTransactionContext(IStaticSyncTransactionContext, ABC):
    @abstractmethod
    async def __call__(self) -> AsyncIterator[None]: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


class IStaticAsyncTransactionContextFactory(ABC):
    @abstractmethod
    def init_transaction_context(self) -> IStaticAsyncTransactionContext: ...
