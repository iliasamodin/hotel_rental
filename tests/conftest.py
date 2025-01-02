from fastapi import FastAPI
from loguru import logger

import pytest
import asyncio

from app.main import app as app_
from app.settings import settings

from tests.db_preparer import DBPreparer


def pytest_addoption(parser):
    parser.addoption(
        "--clean-tables",
        default="1",
        choices=("1", "0"),
    )
    parser.addoption(
        "--deploy-migrations",
        default="1",
        choices=("1", "0"),
    )


@pytest.fixture(scope="session")
def clean_tables(request) -> bool:
    return bool(int(request.config.getoption("--clean-tables")))


@pytest.fixture(scope="session")
def deploy_migrations(request) -> bool:
    return bool(int(request.config.getoption("--deploy-migrations")))


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return app_


def sync_preparing_db(
    db_preparer: DBPreparer,
    deploy_migrations: bool,
) -> None:
    """
    Preparing a test database outside of the event loop.
    """

    db_preparer.deploy_migrations(deploy_migrations=deploy_migrations)


async def async_preparing_db(
    db_preparer: DBPreparer,
    clean_tables: bool,
) -> None:
    """
    Preparing a test database inside of the event loop.
    """

    await db_preparer.setup_db(clean_tables=clean_tables)


@pytest.fixture(scope="session")
def event_loop(
    clean_tables: bool,
    deploy_migrations: bool,
):
    """
    Overrides pytest default function scoped event loop.
    And starts preparing the test database.
    """

    logger.info(f"Connect to {settings.DB_URL}")
    assert settings.MODE == "test"

    db_preparer = DBPreparer()

    sync_preparing_db(
        db_preparer=db_preparer,
        deploy_migrations=deploy_migrations,
    )

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    loop.run_until_complete(
        async_preparing_db(
            db_preparer=db_preparer,
            clean_tables=clean_tables,
        ),
    )

    yield loop

    loop.close()
