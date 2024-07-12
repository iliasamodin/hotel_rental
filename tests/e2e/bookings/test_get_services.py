from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic
from starlette import status

import pytest

from app.db.models.hotels_model import HotelsModel
from app.db.models.hotels_services_model import HotelsServicesModel
from app.db.models.rooms_model import RoomsModel
from app.db.models.rooms_services_model import RoomsServicesModel

from tests.db_preparer import DBPreparer

hotels_for_test = [
    {
        "id": 1,
        "name": "Test hotel #1",
        "location": "Location of the test hotel #1",
    },
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
]
rooms_for_test = [
    {
        "id": 1,
        "hotel_id": 1,
        "ordinal_number": 1,
        "maximum_persons": 2,
        "price": 5_000,
    },
]
service_1_of_rooms_for_test = [
    {
        "room_id": 1,
        "service_variety_id": 1,
    },
]
service_2_of_rooms_for_test = [
    {
        "room_id": 1,
        "service_variety_id": 2,
    },
]


@pytest.mark.asyncio
class TestGetServices:
    """
    E2E tests for GET method of endpoint /services.
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
        self.url = app.url_path_for("get_services")

    @pytest.mark.parametrize(
        argnames=(
            "parameters_of_get",
            "hotels_for_test",
            "services_of_hotels_for_test",
            "rooms_for_test",
            "services_of_rooms_for_test",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                {
                    "only_for_hotels": False,
                    "only_for_rooms": False,
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                service_1_of_rooms_for_test,
                status.HTTP_200_OK,
                [
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
                    {
                        "id": 3, 
                        "key": "spa", 
                        "name": "Availability of spa", 
                        "desc": None,
                    },
                ],
                "Endpoint test for selecting services from the database without filters",
                id="-test-1",
            ),
            pytest.param(
                {
                    "only_for_hotels": True,
                    "only_for_rooms": False,
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                service_1_of_rooms_for_test,
                status.HTTP_200_OK,
                [
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
                    },
                ],
                "Endpoint test for selecting services from the database "
                "with a filter based on the presence of JOINs with hotels",
                id="-test-2",
            ),
            pytest.param(
                {
                    "only_for_hotels": False,
                    "only_for_rooms": True,
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                service_1_of_rooms_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "wifi",
                        "name": "Free Wi-Fi",
                        "desc": None,
                    },
                ],
                "Endpoint test for selecting services from the database "
                "with a filter based on the presence of JOINs with rooms",
                id="-test-3",
            ),
            pytest.param(
                {
                    "only_for_hotels": False,
                    "only_for_rooms": True,
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                service_1_of_rooms_for_test + service_2_of_rooms_for_test,
                status.HTTP_200_OK,
                [
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
                "Endpoint test for selecting services from the database "
                "with a filter based on the presence of JOINs with rooms",
                id="-test-4",
            ),
            pytest.param(
                {
                    "only_for_hotels": True,
                    "only_for_rooms": True,
                },
                hotels_for_test,
                services_of_hotels_for_test,
                rooms_for_test,
                service_1_of_rooms_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": "Service filters for hotels only or rooms only are mutually exclusive.",
                    "extras": {
                        "only_for_hotels": True,
                        "only_for_rooms": True,
                    },
                },
                "Endpoint test for selecting services from the database with invalid filters",
                id="-test-5",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_services(
        self,
        parameters_of_get: dict[str, bool],
        hotels_for_test: list[dict[str, Any]],
        services_of_hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        services_of_rooms_for_test: list[dict[str, Any]],
        expected_status_code: int,
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
            self.db_preparer.insert_test_data(
                orm_model=RoomsServicesModel,
                data_for_insert=services_of_rooms_for_test,
            ),
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
