from typing import Iterable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from importlib import import_module

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


def load_model(package_name: str, module_name: str, class_name: str | None = None) -> object:
    """
    Dynamic import of class.

    :return: object
    """

    module = import_module(f"{package_name}.{module_name}")

    if class_name is not None:
        Class = getattr(module, class_name)
    else:    
        Class = getattr(
            module, 
            "".join((word.capitalize() for word in module_name.split("_"))),
        )

    return Class
