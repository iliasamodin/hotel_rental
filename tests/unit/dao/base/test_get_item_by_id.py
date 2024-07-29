from contextlib import AbstractContextManager, nullcontext as does_not_raise
from fastapi import FastAPI
from icecream import ic

import pytest

from app.db.models.service_varieties_model import ServiceVarietiesModel

from app.dao.base.dao import BaseDAO
from app.dao.base.exceptions import ModelNotFoundError

from tests.db_preparer import DBPreparer
from tests.fake_session import FakeAsyncSession


@pytest.mark.asyncio
class TestGetItemById:
    """
    Unit tests for method get_item_by_id of BaseDAO class.
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
            "item_id",
            "expected_result",
            "expectation",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                ServiceVarietiesModel.__tablename__,
                1,
                "SELECT "
                "booking.service_varieties.id, "
                "booking.service_varieties.key, "
                "booking.service_varieties.name, "
                "booking.service_varieties.\"desc\" \n"
                "FROM booking.service_varieties \n"
                "WHERE booking.service_varieties.id = 1",
                does_not_raise(),
                "Testing a query to select a record by its ID.",
                id="-test-1",
            ),
            pytest.param(
                "non_existent_table",
                1,
                None,
                pytest.raises(ModelNotFoundError),
                "Testing a query to select a record by its ID "
                "from a non-existent table.",
                id="-test-2",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_item_by_id(
        self,
        table_name: str,
        item_id: int,
        expected_result: str | None,
        expectation: AbstractContextManager,
        test_description: str,
    ):
        ic(test_description)

        # Context manager for catching and checking exceptions
        #   raised by the object under test
        with expectation:
            base_dao = BaseDAO(session=self.fake_async_session)
            await base_dao.get_item_by_id(
                table_name=table_name,
                item_id=item_id,
            )

            sql_query = self.fake_async_session.query

            assert sql_query == expected_result, "The sql query is not as expected"
