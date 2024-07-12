from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic
from starlette import status

import pytest

from app.db.models.rooms_model import RoomsModel
from app.db.models.hotels_model import HotelsModel

from tests.db_preparer import DBPreparer

hotels_for_test = [
    {
        "id": 1,
        "name": "Test hotel #1",
        "location": "Location of the test hotel #1",
    },
    {
        "id": 2,
        "name": "Test hotel #2",
        "location": "Location of the test hotel #2",
    },
]
rooms_for_test = [
    {
        "id": 1,
        "hotel_id": 1,
        "premium_level_id": 1,
        "ordinal_number": 1,
        "maximum_persons": 2,
        "price": 5_000,
    },
    {
        "id": 2,
        "hotel_id": 1,
        "premium_level_id": 2,
        "ordinal_number": 2,
        "maximum_persons": 2,
        "price": 5_000,
    },
    {
        "id": 3,
        "hotel_id": 2,
        "premium_level_id": 3,
        "ordinal_number": 1,
        "maximum_persons": 2,
        "price": 5_000,
    },
]


@pytest.mark.asyncio
class TestPremiumLevels:
    """
    E2E tests for GET method of endpoint /premium-levels.
    """

    @pytest.fixture(autouse=True)
    def init(
        self,
        app: FastAPI,
        transport_for_client: ASGITransport,
        client_maker: AsyncClient = AsyncClient,
        db_preparer: DBPreparer = DBPreparer,
    ):
        self.app = app
        self.transport_for_client = transport_for_client
        self.client_maker = client_maker
        self.db_preparer = db_preparer()
        self.url = app.url_path_for("get_premium_levels")

    @pytest.mark.parametrize(
        argnames=(
            "parameters_of_get",
            "hotels_for_test",
            "rooms_for_test",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                None,
                hotels_for_test,
                rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "budget",
                        "name": "Budget service",
                        "desc": "Minimum service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 2,
                        "key": "comfort",
                        "name": "Comfort service",
                        "desc": "Average service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 3,
                        "key": "premium",
                        "name": "Premium service",
                        "desc": "Premium service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 4,
                        "key": "presidential",
                        "name": "Presidential service",
                        "desc": "Presidential service.",
                    },
                ],
                "Endpoint test for selecting room's premium levels from the database without filters",
                id="-test-1",
            ),
            pytest.param(
                {
                    "hotel_id": 1,
                },
                hotels_for_test,
                rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "budget",
                        "name": "Budget service",
                        "desc": "Minimum service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 2,
                        "key": "comfort",
                        "name": "Comfort service",
                        "desc": "Average service for the level of the hotel to which the room belongs.",
                    },
                ],
                "Endpoint test for selecting room's premium levels from the database "
                "with a filter by hotel ID",
                id="-test-2",
            ),
            pytest.param(
                {
                    "hotel_id": 3,
                },
                hotels_for_test,
                rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting room's premium levels from the database "
                "with filter by non-existent hotel ID",
                id="-test-3",
            ),
            pytest.param(
                {
                    "connected_with_rooms": True,
                },
                hotels_for_test,
                rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "budget",
                        "name": "Budget service",
                        "desc": "Minimum service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 2,
                        "key": "comfort",
                        "name": "Comfort service",
                        "desc": "Average service for the level of the hotel to which the room belongs.",
                    },
                    {
                        "id": 3,
                        "key": "premium",
                        "name": "Premium service",
                        "desc": "Premium service for the level of the hotel to which the room belongs.",
                    },
                ],
                "Endpoint test for selecting room's premium levels from the database "
                "with a filter based on the presence of connections between premium levels and hotel's rooms",
                id="-test-4",
            ),
            pytest.param(
                {
                    "hotel_id": 2,
                    "connected_with_rooms": True,
                },
                hotels_for_test,
                rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 3,
                        "key": "premium",
                        "name": "Premium service",
                        "desc": "Premium service for the level of the hotel to which the room belongs.",
                    },
                ],
                "Endpoint test for selecting room's premium levels from the database "
                "with a filter by hotel ID and the presence of connections between premium levels and hotel's rooms",
                id="-test-5",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_premium_levels(
        self,
        parameters_of_get: dict[str, Any] | None,
        hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        expected_status_code: int,
        expected_result: list[dict[str, Any]],
        test_description: str,
    ):
        ic(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with (
            self.db_preparer.insert_test_data(orm_model=HotelsModel, data_for_insert=hotels_for_test),
            self.db_preparer.insert_test_data(orm_model=RoomsModel, data_for_insert=rooms_for_test),
        ):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.get(
                    url=f"http://test{self.url}",
                    params=parameters_of_get,
                )

                status_code_of_response = api_response.status_code
                ic(status_code_of_response)
                dict_of_response = api_response.json()
                ic(dict_of_response)

            assert (
                status_code_of_response == expected_status_code,
                "The status code returned by the endpoint is not as expected",
            )
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
