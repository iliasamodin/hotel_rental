from contextlib import AbstractContextManager, nullcontext as does_not_raise
from fastapi import FastAPI
from loguru import logger

import pytest

from app.adapters.secondary.db.models.service_varieties_model import ServiceVarietiesModel

from app.adapters.secondary.db.dao.base.dao import BaseDAO
from app.adapters.secondary.db.dao.base.exceptions import ModelNotFoundError

from tests.db_preparer import DBPreparer
from tests.fake_transaction_context import FakeStaticAsyncTransactionContext


@pytest.mark.asyncio
class TestInsertItem:
    """
    Unit tests for method insert_item of BaseDAO class.
    """

    @pytest.fixture(autouse=True)
    def init(
        self,
        app: FastAPI,
        db_preparer: DBPreparer = DBPreparer,
        fake_transaction_context: FakeStaticAsyncTransactionContext = FakeStaticAsyncTransactionContext,
    ):
        self.app = app
        self.db_preparer = db_preparer()
        self.fake_transaction_context = fake_transaction_context(engine=self.db_preparer.engine)

    @pytest.mark.parametrize(
        argnames=(
            "table_name",
            "item_data",
            "expected_result",
            "expectation",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                ServiceVarietiesModel.__tablename__,
                {
                    "key": "wifi",
                    "desc": "Free Wi-Fi",
                },
                'INSERT INTO booking.service_varieties (key, "desc") '
                "VALUES ('wifi', 'Free Wi-Fi') "
                "RETURNING "
                "booking.service_varieties.id, "
                "booking.service_varieties.key, "
                "booking.service_varieties.name, "
                'booking.service_varieties."desc"',
                does_not_raise(),
                "Testing a query to insert a record",
                id="-test-1",
            ),
            pytest.param(
                "non_existent_table",
                {
                    "title": "wifi",
                    "desc": "Free Wi-Fi",
                },
                None,
                pytest.raises(ModelNotFoundError),
                "Testing a query to insert a record into non-existent table",
                id="-test-2",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_insert_item(
        self,
        table_name: str,
        item_data: int,
        expected_result: str | None,
        expectation: AbstractContextManager,
        test_description: str,
    ):
        logger.info(test_description)

        # Context manager for catching and checking exceptions
        #   raised by the object under test
        with expectation:
            base_dao = BaseDAO()
            await base_dao.insert_item(
                transaction_context=self.fake_transaction_context,
                table_name=table_name,
                item_data=item_data,
            )

            sql_query = self.fake_transaction_context.query

            assert sql_query == expected_result, "The sql query is not as expected"
