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
class TestDeleteItemById:
    """
    Unit tests for method delete_item_by_id of BaseDAO class.
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
            "item_id",
            "expected_result",
            "expectation",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                ServiceVarietiesModel.__tablename__,
                1,
                "DELETE FROM booking.service_varieties "
                "WHERE booking.service_varieties.id = 1 "
                "RETURNING "
                "booking.service_varieties.id, "
                "booking.service_varieties.key, "
                "booking.service_varieties.name, "
                'booking.service_varieties."desc"',
                does_not_raise(),
                "Testing a query to delete a record by its ID",
                id="-test-1",
            ),
            pytest.param(
                "non_existent_table",
                1,
                None,
                pytest.raises(ModelNotFoundError),
                "Testing a query to delete a record by its ID from a non-existent table",
                id="-test-2",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_delete_item_by_id(
        self,
        table_name: str,
        item_id: int,
        expected_result: str | None,
        expectation: AbstractContextManager,
        test_description: str,
    ):
        logger.info(test_description)

        # Context manager for catching and checking exceptions
        #   raised by the object under test
        with expectation:
            base_dao = BaseDAO()
            await base_dao.delete_item_by_id(
                transaction_context=self.fake_transaction_context,
                table_name=table_name,
                item_id=item_id,
            )

            sql_query = self.fake_transaction_context.query

            assert sql_query == expected_result, "The sql query is not as expected"
