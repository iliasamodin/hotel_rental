from typing import Iterable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.settings import settings


async def create_schemas(
    db_url: str = settings.DB_SECRET_URL,
    schemas: Iterable = (settings.DB_BOOKING_SCHEMA, settings.DB_ALEMBIC_SCHEMA),
) -> None:
    """
    Create schemas in datadase if they don't exist.
    """

    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as connect:
        for schema in schemas:
            await connect.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}";'))
