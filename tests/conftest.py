from fastapi import FastAPI
from icecream import ic

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


@pytest.fixture(scope="session")
def clean_tables(request) -> bool:
    return bool(int(request.config.getoption("--clean-tables")))


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return app_


async def preparing_db_for_tests(clean_tables: bool) -> None:
    """
    Checking in the fixture that the tests are executed 
    on the test base, 
    otherwise, the tests are not run. 
    """

    ic(f"Connect to {settings.DB_URL}")
    assert settings.MODE == "test"

    db_preparer = DBPreparer()

    await db_preparer.setup_db(clean_tables=clean_tables)


@pytest.fixture(scope="session")
def event_loop(clean_tables):
    """
    Overrides pytest default function scoped event loop.
    """

    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    loop.run_until_complete(preparing_db_for_tests(clean_tables=clean_tables))

    yield loop

    loop.close()
