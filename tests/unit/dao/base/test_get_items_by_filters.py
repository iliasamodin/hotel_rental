from contextlib import AbstractContextManager, nullcontext as does_not_raise
from fastapi import FastAPI
from loguru import logger

import pytest

from app.adapters.secondary.db.models.service_varieties_model import ServiceVarietiesModel

from app.adapters.secondary.db.dao.base.dao import BaseDAO
from app.adapters.secondary.db.dao.base.exceptions import ModelNotFoundError

from tests.db_preparer import DBPreparer
from tests.fake_session import FakeAsyncSession


@pytest.mark.asyncio
class TestGetItemsByFilters:
    """
    Unit tests for method get_items_by_filters of BaseDAO class.
    """

    @pytest.fixture(autouse=True)
    def init(
        self,
        app: FastAPI,
        db_preparer: DBPreparer = DBPreparer,
        fake_async_session: FakeAsyncSession = FakeAsyncSession,
    ):
        self.app = app
        self.db_preparer = db_preparer()
        self.fake_async_session = fake_async_session(engine=self.db_preparer.engine)

    @pytest.mark.parametrize(
        argnames=(
            "table_name",
            "filters",
            "expected_result",
            "expectation",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                ServiceVarietiesModel.__tablename__,
                {
                    "key": "wifi",
                },
                "SELECT "
                "booking.service_varieties.id, "
                "booking.service_varieties.key, "
                "booking.service_varieties.name, "
                'booking.service_varieties."desc" \n'
                "FROM booking.service_varieties \n"
                "WHERE "
                "booking.service_varieties.key = 'wifi'",
                does_not_raise(),
                "Testing a query to select a record by filters",
                id="-test-1",
            ),
            pytest.param(
                "non_existent_table",
                {
                    "key": "wifi",
                },
                None,
                pytest.raises(ModelNotFoundError),
                "Testing a query to select a records by filters from a non-existent table",
                id="-test-2",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_items_by_filters(
        self,
        table_name: str,
        filters: dict[str, str],
        expected_result: str | None,
        expectation: AbstractContextManager,
        test_description: str,
    ):
        logger.info(test_description)

        # Context manager for catching and checking exceptions
        #   raised by the object under test
        with expectation:
            base_dao = BaseDAO()
            base_dao.session = self.fake_async_session
            await base_dao.get_items_by_filters(
                table_name=table_name,
                filters=filters,
            )

            sql_query = self.fake_async_session.query

            assert sql_query == expected_result, "The sql query is not as expected"
