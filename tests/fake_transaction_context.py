from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncEngine


class FakeStaticAsyncTransactionContext:
    """
    Fake context of the database connection.
    """

    _sql_query: str

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    def __getattr__(self, name: str):
        return self

    def __call__(self, *args, **kwargs):
        return self

    async def execute(self, query: Select):
        self._sql_query = query.compile(
            bind=self.engine,
            compile_kwargs={
                "literal_binds": True,
            },
        )

        return self

    async def commit(self):
        return self

    @property
    def query(self):
        return str(self._sql_query)
