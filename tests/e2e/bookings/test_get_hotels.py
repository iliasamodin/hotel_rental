from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic

import pytest

from app.db.models.hotels_model import HotelsModel
from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.rooms_model import RoomsModel

from tests.db_preparer import DBPreparer

hotels_for_test = [
    {
        "id": 1,
        "name": "Test hotel #1",
        "desc": "Colorful description for hotel #1.",
        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
        "stars": 5,
    },
    {
        "id": 2,
        "name": "Test hotel #2",
        "desc": "Colorful description for hotel #2.",
        "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
        "stars": None,
    },
    {
        "id": 3,
        "name": "Test hotel #3",
        "desc": "Colorful description for hotel #3.",
        "location": "Komi Republic, Syktyvkar, Kommunisticheskaya street, 67",
        "stars": 4,
    }
]
services_of_hotels_for_test = [
    {
        "hotel_id": 1,
        "service_variety_id": 1,
    },
    {
        "hotel_id": 1,
        "service_variety_id": 3,
    },
    {
        "hotel_id": 2,
        "service_variety_id": 1,
    },
]
rooms_for_test = [
    {
        "id": 1,
        "hotel_id": 1,
        "ordinal_number": 1,
        "maximum_persons": 2,
        "price": 5000,
    },
    {
        "id": 2,
        "hotel_id": 2,
        "ordinal_number": 1,
        "maximum_persons": 3,
        "price": 5000,
    },
    {
        "id": 3,
        "hotel_id": 3,
        "ordinal_number": 1,
        "maximum_persons": 3,
        "price": 5000,
    },
]


@pytest.mark.asyncio
class TestGetHotels:
    """
    E2E tests for endpoint /get-hotels.
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
        self.url = app.url_path_for("get_hotels")

    @pytest.mark.parametrize(
        argnames=(
            "parameters_of_get",
            "body_of_request",
            "hotels_for_test",
            "services_of_hotels_for_test",
            "rooms_for_test",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                None,
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 1,
                        "name": "Test hotel #1",
                        "desc": "Colorful description for hotel #1.",
                        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                        "stars": 5,
                        "rooms_quantity": 1,
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 3,
                                "key": "spa",
                                "name": "Availability of spa",
                                "desc": None,
                            }
                        ],
                    },
                    {
                        "id": 2,
                        "name": "Test hotel #2",
                        "desc": "Colorful description for hotel #2.",
                        "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                        "stars": None,
                        "rooms_quantity": 1,
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
                        "name": "Test hotel #3",
                        "desc": "Colorful description for hotel #3.",
                        "location": "Komi Republic, Syktyvkar, Kommunisticheskaya street, 67",
                        "stars": 4,
                        "rooms_quantity": 1,
                        "services": [],
                    },
                ],
                "Endpoint test for selecting hotels from the database without filters",
                id="-test-1",
            ),
            pytest.param(
                {
                    "location": "Komi",
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 3,
                        "name": "Test hotel #3",
                        "desc": "Colorful description for hotel #3.",
                        "location": "Komi Republic, Syktyvkar, Kommunisticheskaya street, 67",
                        "stars": 4,
                        "rooms_quantity": 1,
                        "services": [],
                    },
                ],
                "Endpoint test for selecting hotels from the database "
                "with filter by location",
                id="-test-2",
            ),
            pytest.param(
                {
                    "location": "London",
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [],
                "Endpoint test for selecting hotels "
                "with a filter by location for which there are no hotels in the database",
                id="-test-3",
            ),
            pytest.param(
                {
                    "number_of_guests": 3,
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 2,
                        "name": "Test hotel #2",
                        "desc": "Colorful description for hotel #2.",
                        "location": "Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a",
                        "stars": None,
                        "rooms_quantity": 1,
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
                        "name": "Test hotel #3",
                        "desc": "Colorful description for hotel #3.",
                        "location": "Komi Republic, Syktyvkar, Kommunisticheskaya street, 67",
                        "stars": 4,
                        "rooms_quantity": 1,
                        "services": [],
                    },
                ],
                "Endpoint test for selecting hotels from the database "
                "with a filter based on the number of people wishing to stay in one hotel room",
                id="-test-4",
            ),
            pytest.param(
                {
                    "number_of_guests": 10,
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [],
                "Endpoint test for selecting hotels "
                "with a filter by the number of persons that exceeds all existing hotel rooms in the database",
                id="-test-5",
            ),
            pytest.param(
                {
                    "stars": 5,
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 1,
                        "name": "Test hotel #1",
                        "desc": "Colorful description for hotel #1.",
                        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                        "stars": 5,
                        "rooms_quantity": 1,
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 3,
                                "key": "spa",
                                "name": "Availability of spa",
                                "desc": None,
                            }
                        ],
                    },
                ],
                "Endpoint test for selecting hotels from the database "
                "with a filter by the number of stars of the hotel",
                id="-test-6",
            ),
            pytest.param(
                {
                    "stars": 6,
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [],
                "Endpoint test for selecting hotels "
                "with a filter based on the number of stars for hotels, "
                "which exceeds the number of stars for all hotels in the database",
                id="-test-7",
            ),
            pytest.param(
                None,
                {
                    "service_ids": [1, 3],
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 1,
                        "name": "Test hotel #1",
                        "desc": "Colorful description for hotel #1.",
                        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                        "stars": 5,
                        "rooms_quantity": 1,
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 3,
                                "key": "spa",
                                "name": "Availability of spa",
                                "desc": None,
                            }
                        ],
                    },
                ],
                "Endpoint test for selecting hotels from the database "
                "with filter by hotel service",
                id="-test-8",
            ),
            pytest.param(
                None,
                {
                    "service_ids": [1, 2, 3],
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [],
                "Endpoint test for selecting hotels from the database "
                "with a filter by service that is not associated with any of the hotels",
                id="-test-9",
            ),
            pytest.param(
                {
                    "location": "Altai",
                    "number_of_guests": 2,
                    "stars": 5,
                },
                {
                    "service_ids": [1, 3],
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                [
                    {
                        "id": 1,
                        "name": "Test hotel #1",
                        "desc": "Colorful description for hotel #1.",
                        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
                        "stars": 5,
                        "rooms_quantity": 1,
                        "services": [
                            {
                                "id": 1,
                                "key": "wifi",
                                "name": "Free Wi-Fi",
                                "desc": None,
                            },
                            {
                                "id": 3,
                                "key": "spa",
                                "name": "Availability of spa",
                                "desc": None,
                            }
                        ],
                    },
                ],
                "Endpoint test for selecting hotels from the database with all filters",
                id="-test-10",
            ),
            pytest.param(
                {
                    "stars": 10,
                },
                None,
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                {
                    "detail": [
                        {
                            "ctx": {
                                "le": 6,
                            },
                            "input": "10",
                            "loc": [
                                "query",
                                "stars",
                            ],
                            "msg": "Input should be less than or equal to 6",
                            "type": "less_than_equal",
                            "url": "https://errors.pydantic.dev/2.6/v/less_than_equal",
                        },
                    ],
                },
                "Endpoint test for selecting hotels from the database "
                "with a filter based on the number of stars exceeding the allowed number",
                id="-test-11",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_hotels(
        self,
        parameters_of_get: dict[str, bool] | None,
        body_of_request: dict[str, list[int]] | None,
        hotels_for_test: list[dict[str, Any]],
        services_of_hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        expected_result: list[dict[str, Any]] | dict[str, Any],
        test_description: str,
    ):
        ic(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with (
            self.db_preparer.insert_test_data(orm_model=HotelsModel, data_for_insert=hotels_for_test),
            self.db_preparer.insert_test_data(
                orm_model=HotelsServicesModel, 
                data_for_insert=services_of_hotels_for_test,
            ),
            self.db_preparer.insert_test_data(orm_model=RoomsModel, data_for_insert=rooms_for_test),
        ):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.post(
                    url=f"http://test{self.url}",
                    params=parameters_of_get,
                    json=body_of_request,
                )
                dict_of_response = api_response.json()
                ic(dict_of_response)

            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
