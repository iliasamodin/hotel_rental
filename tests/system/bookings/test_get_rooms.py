from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from loguru import logger
from starlette import status

import pytest

from app.adapters.secondary.db.models.hotels_model import HotelsModel
from app.adapters.secondary.db.models.rooms_model import RoomsModel
from app.adapters.secondary.db.models.rooms_services_model import RoomsServicesModel

from tests.db_preparer import DBPreparer

hotels_for_test = [
    {
        "id": 1,
        "name": "Test hotel #1",
        "desc": "Colorful description for hotel #1.",
        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
        "stars": 3,
    },
    {
        "id": 2,
        "name": "Test hotel #2",
        "desc": "Colorful description for hotel #2.",
        "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
        "stars": 5,
    },
]
rooms_for_test = [
    {
        "id": 1,
        "name": "Room #1 of hotel #1",
        "desc": "Colorful description for room #1 of hotel #1.",
        "hotel_id": 1,
        "premium_level_id": None,
        "ordinal_number": 1,
        "maximum_persons": 2,
        "price": 5_000,
    },
    {
        "id": 2,
        "name": "Room #2 of hotel #1",
        "desc": "Colorful description for room #2 of hotel #1.",
        "hotel_id": 1,
        "premium_level_id": 2,
        "ordinal_number": 2,
        "maximum_persons": 3,
        "price": 10_000,
    },
    {
        "id": 3,
        "name": "Room #1 of hotel #2",
        "desc": "Colorful description for room #1 of hotel #2.",
        "hotel_id": 2,
        "premium_level_id": 4,
        "ordinal_number": 1,
        "maximum_persons": 3,
        "price": 50_000,
    },
]
services_of_rooms_for_test = [
    {
        "room_id": 2,
        "service_variety_id": 1,
    },
    {
        "room_id": 3,
        "service_variety_id": 1,
    },
    {
        "room_id": 3,
        "service_variety_id": 2,
    },
]


@pytest.mark.asyncio
class TestGetRooms:
    """
    System tests for GET method of endpoint /rooms.
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
        self.url = app.url_path_for("get_rooms")

    @pytest.mark.parametrize(
        argnames=(
            "query_params",
            "hotels_for_test",
            "rooms_for_test",
            "services_of_rooms_for_test",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                None,
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "name": "Room #1 of hotel #1",
                        "desc": "Colorful description for room #1 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": None,
                        "ordinal_number": 1,
                        "maximum_persons": 2,
                        "price": 5_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": None,
                        "services": [],
                    },
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "name": "Room #1 of hotel #2",
                        "desc": "Colorful description for room #1 of hotel #2.",
                        "hotel_id": 2,
                        "premium_level_id": 4,
                        "ordinal_number": 1,
                        "maximum_persons": 3,
                        "price": 50_000,
                        "hotel": {
                            "id": 2,
                            "name": "Test hotel #2",
                            "desc": "Colorful description for hotel #2.",
                            "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                            "stars": 5,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 4,
                            "key": "presidential",
                            "name": "Presidential service",
                            "desc": "Presidential service.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 2,
                                "key": "pool",
                                "name": "Swimming pool",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database without filters",
                id="-test-1",
            ),
            pytest.param(
                {
                    "min_price": 10_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "name": "Room #1 of hotel #2",
                        "desc": "Colorful description for room #1 of hotel #2.",
                        "hotel_id": 2,
                        "premium_level_id": 4,
                        "ordinal_number": 1,
                        "maximum_persons": 3,
                        "price": 50_000,
                        "hotel": {
                            "id": 2,
                            "name": "Test hotel #2",
                            "desc": "Colorful description for hotel #2.",
                            "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                            "stars": 5,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 4,
                            "key": "presidential",
                            "name": "Presidential service",
                            "desc": "Presidential service.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 2,
                                "key": "pool",
                                "name": "Swimming pool",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database "
                "with a filter based on the minimum room rental price",
                id="-test-2",
            ),
            pytest.param(
                {
                    "min_price": 100_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting rooms from the database "
                "with a filter based on the minimum price for renting a room "
                "that exceeds the cost of renting any of the rooms existing in the database",
                id="-test-3",
            ),
            pytest.param(
                {
                    "max_price": 10_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "name": "Room #1 of hotel #1",
                        "desc": "Colorful description for room #1 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": None,
                        "ordinal_number": 1,
                        "maximum_persons": 2,
                        "price": 5_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": None,
                        "services": [],
                    },
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database "
                "with a filter based on the maximum room rental price",
                id="-test-4",
            ),
            pytest.param(
                {
                    "max_price": 1_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting rooms from the database "
                "with a filter based on the maximum room rental price less than the rental cost of any existing room",
                id="-test-5",
            ),
            pytest.param(
                {
                    "min_price": 10_000,
                    "max_price": 10_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database "
                "With filters for the minimum and maximum room rental price",
                id="-test-6",
            ),
            pytest.param(
                {
                    "hotel_id": 1,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "name": "Room #1 of hotel #1",
                        "desc": "Colorful description for room #1 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": None,
                        "ordinal_number": 1,
                        "maximum_persons": 2,
                        "price": 5_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": None,
                        "services": [],
                    },
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database with a filter by hotel ID",
                id="-test-7",
            ),
            pytest.param(
                {
                    "hotel_id": 3,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting rooms from the database with filter by non-existent hotel ID",
                id="-test-8",
            ),
            pytest.param(
                {
                    "number_of_guests": 3,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                    {
                        "id": 3,
                        "name": "Room #1 of hotel #2",
                        "desc": "Colorful description for room #1 of hotel #2.",
                        "hotel_id": 2,
                        "premium_level_id": 4,
                        "ordinal_number": 1,
                        "maximum_persons": 3,
                        "price": 50_000,
                        "hotel": {
                            "id": 2,
                            "name": "Test hotel #2",
                            "desc": "Colorful description for hotel #2.",
                            "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                            "stars": 5,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 4,
                            "key": "presidential",
                            "name": "Presidential service",
                            "desc": "Presidential service.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 2,
                                "key": "pool",
                                "name": "Swimming pool",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database with filter by number of guests",
                id="-test-9",
            ),
            pytest.param(
                {
                    "number_of_guests": 10,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting rooms from the database "
                "with a filter by the number of guests exceeding the capacity of any of the rooms in the database",
                id="-test-10",
            ),
            pytest.param(
                {
                    "premium_levels": [2, 3],
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 2,
                        "name": "Room #2 of hotel #1",
                        "desc": "Colorful description for room #2 of hotel #1.",
                        "hotel_id": 1,
                        "premium_level_id": 2,
                        "ordinal_number": 2,
                        "maximum_persons": 3,
                        "price": 10_000,
                        "hotel": {
                            "id": 1,
                            "name": "Test hotel #1",
                            "desc": "Colorful description for hotel #1.",
                            "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                            "stars": 3,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 2,
                            "key": "comfort",
                            "name": "Comfort service",
                            "desc": "Average service for the level of the hotel to which the room belongs.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database with filtering by premium levels",
                id="-test-11",
            ),
            pytest.param(
                {
                    "premium_levels": [3, 5],
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting rooms from the database "
                "with filtering by premium levels for which there are no rooms in the database",
                id="-test-12",
            ),
            pytest.param(
                {
                    "services": [1, 2],
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 3,
                        "name": "Room #1 of hotel #2",
                        "desc": "Colorful description for room #1 of hotel #2.",
                        "hotel_id": 2,
                        "premium_level_id": 4,
                        "ordinal_number": 1,
                        "maximum_persons": 3,
                        "price": 50_000,
                        "hotel": {
                            "id": 2,
                            "name": "Test hotel #2",
                            "desc": "Colorful description for hotel #2.",
                            "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                            "stars": 5,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 4,
                            "key": "presidential",
                            "name": "Presidential service",
                            "desc": "Presidential service.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 2,
                                "key": "pool",
                                "name": "Swimming pool",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database with filtering by room service",
                id="-test-13",
            ),
            pytest.param(
                {
                    "min_price": 35_000,
                    "max_price": 100_000,
                    "hotel_id": 2,
                    "number_of_guests": 2,
                    "premium_levels": [4],
                    "services": [1, 2],
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 3,
                        "name": "Room #1 of hotel #2",
                        "desc": "Colorful description for room #1 of hotel #2.",
                        "hotel_id": 2,
                        "premium_level_id": 4,
                        "ordinal_number": 1,
                        "maximum_persons": 3,
                        "price": 50_000,
                        "hotel": {
                            "id": 2,
                            "name": "Test hotel #2",
                            "desc": "Colorful description for hotel #2.",
                            "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                            "stars": 5,
                            "main_image_id": None,
                        },
                        "premium_level": {
                            "id": 4,
                            "key": "presidential",
                            "name": "Presidential service",
                            "desc": "Presidential service.",
                        },
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 2,
                                "key": "pool",
                                "name": "Swimming pool",
                                "desc": None,
                            },
                        ],
                    },
                ],
                "Endpoint test for selecting rooms from the database all filters",
                id="-test-14",
            ),
            pytest.param(
                {
                    "min_price": 100_000,
                    "max_price": 35_000,
                },
                hotels_for_test,
                rooms_for_test,
                services_of_rooms_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": "The minimum room price filter must be less than the maximum room price filter.",
                    "extras": {
                        "min_price": 100_000,
                        "max_price": 35_000,
                    },
                },
                "Endpoint test for selecting rooms from the database with an invalid price range as a filter",
                id="-test-15",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_rooms(
        self,
        query_params: dict[str, Any] | None,
        hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        services_of_rooms_for_test: list[dict[str, Any]],
        expected_status_code: int,
        expected_result: list[dict[str, Any]] | dict[str, Any],
        test_description: str,
    ):
        logger.info(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with (
            self.db_preparer.insert_test_data(orm_model=HotelsModel, data_for_insert=hotels_for_test),
            self.db_preparer.insert_test_data(orm_model=RoomsModel, data_for_insert=rooms_for_test),
            self.db_preparer.insert_test_data(
                orm_model=RoomsServicesModel,
                data_for_insert=services_of_rooms_for_test,
            ),
        ):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.get(
                    url=f"http://test{self.url}",
                    params=query_params,
                )

                status_code_of_response = api_response.status_code
                logger.debug(status_code_of_response)
                dict_of_response = api_response.json()
                logger.debug(dict_of_response)

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
