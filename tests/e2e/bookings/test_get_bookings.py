from datetime import datetime
from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic
from starlette import status

import pytest

from app.settings import settings

from app.db.models.bookings_model import BookingsModel
from app.db.models.hotels_model import HotelsModel
from app.db.models.rooms_model import RoomsModel
from app.db.models.users_model import UsersModel

from app.services.authorization.helpers import get_password_hash, get_access_token
from app.services.authorization.schemas import UserResponseSchema

from tests.db_preparer import DBPreparer

cookies_of_first_user = {
    settings.ACCESS_TOKEN_COOKIE: get_access_token(
        user=UserResponseSchema(
            id=1,
            email="user1@example.com",
            phone="+7-999-999-99-97",
            first_name="Freddie",
            last_name="Mercury",
        )
    ).token
}

hotels_for_test = [
    {
        "id": 1,
        "name": "Test hotel #1",
        "desc": "Colorful description for hotel #1.",
        "location": "Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20",
        "stars": 3,
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
]
users_for_test = [
    {
        "id": 1,
        "email": "user1@example.com",
        "phone": "+7-999-999-99-97",
        "first_name": "Freddie",
        "last_name": "Mercury",
        "password": get_password_hash(password="Password1"),
    },
    {
        "id": 2,
        "email": "user2@example.com",
        "phone": "+7-999-999-99-98",
        "first_name": "Carlton",
        "last_name": "Williams",
        "password": get_password_hash(password="Password2"),
    },
]
bookings_for_test = [
    {
        "id": 1,
        "user_id": 1,
        "room_id": 1,
        "number_of_persons": 1,
        "check_in_dt": datetime(year=2024, month=7, day=2, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=7, day=3, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 5_000,
    },
    {
        "id": 2,
        "user_id": 2,
        "room_id": 2,
        "number_of_persons": 1,
        "check_in_dt": datetime(year=2024, month=7, day=2, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=7, day=3, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 10_000,
    },
    {
        "id": 3,
        "user_id": 1,
        "room_id": 2,
        "number_of_persons": 2,
        "check_in_dt": datetime(year=2024, month=8, day=10, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=8, day=22, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 110_000,
    },
    {
        "id": 4,
        "user_id": 1,
        "room_id": 1,
        "number_of_persons": 2,
        "check_in_dt": datetime(year=2025, month=9, day=10, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2025, month=9, day=22, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 55_000,
    },
]


@pytest.mark.asyncio
class TestGetBookings:
    """
    E2E tests for GET method of endpoint /bookings.
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
        self.url = app.url_path_for("get_bookings")

    @pytest.mark.parametrize(
        argnames=(
            "query_params",
            "cookies",
            "hotels_for_test",
            "rooms_for_test",
            "users_for_test",
            "bookings_for_test",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                None,
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "user_id": 1,
                        "room_id": 1,
                        "number_of_persons": 1,
                        "check_in_dt": "2024-07-02T14:00:00Z",
                        "check_out_dt": "2024-07-03T12:00:00Z",
                        "total_cost": 5_000,
                        "room": {
                            "id": 1,
                            "name": "Room #1 of hotel #1",
                            "desc": "Colorful description for room #1 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": None,
                            "ordinal_number": 1,
                            "maximum_persons": 2,
                            "price": 5_000,
                        },
                    },
                    {
                        "id": 3,
                        "user_id": 1,
                        "room_id": 2,
                        "number_of_persons": 2,
                        "check_in_dt": "2024-08-10T14:00:00Z",
                        "check_out_dt": "2024-08-22T12:00:00Z",
                        "total_cost": 110_000,
                        "room": {
                            "id": 2,
                            "name": "Room #2 of hotel #1",
                            "desc": "Colorful description for room #2 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": 2,
                            "ordinal_number": 2,
                            "maximum_persons": 3,
                            "price": 10_000,
                        },
                    },
                    {
                        "id": 4,
                        "user_id": 1,
                        "room_id": 1,
                        "number_of_persons": 2,
                        "check_in_dt": "2025-09-10T14:00:00Z",
                        "check_out_dt": "2025-09-22T12:00:00Z",
                        "total_cost": 55_000,
                        "room": {
                            "id": 1,
                            "name": "Room #1 of hotel #1",
                            "desc": "Colorful description for room #1 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": None,
                            "ordinal_number": 1,
                            "maximum_persons": 2,
                            "price": 5_000,
                        },
                    },
                ],
                "Endpoint test for selecting user's bookings from the database without filters",
                id="-test-1",
            ),
            pytest.param(
                {
                    "min_dt": "2024-08-16T14:00:00Z",
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 4,
                        "user_id": 1,
                        "room_id": 1,
                        "number_of_persons": 2,
                        "check_in_dt": "2025-09-10T14:00:00Z",
                        "check_out_dt": "2025-09-22T12:00:00Z",
                        "total_cost": 55_000,
                        "room": {
                            "id": 1,
                            "name": "Room #1 of hotel #1",
                            "desc": "Colorful description for room #1 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": None,
                            "ordinal_number": 1,
                            "maximum_persons": 2,
                            "price": 5_000,
                        },
                    },
                ],
                "Endpoint test for selecting user's bookings from the database "
                "with filter by minimum check in date",
                id="-test-2",
            ),
            pytest.param(
                {
                    "max_dt": "2024-08-16T12:00:00Z",
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "user_id": 1,
                        "room_id": 1,
                        "number_of_persons": 1,
                        "check_in_dt": "2024-07-02T14:00:00Z",
                        "check_out_dt": "2024-07-03T12:00:00Z",
                        "total_cost": 5_000,
                        "room": {
                            "id": 1,
                            "name": "Room #1 of hotel #1",
                            "desc": "Colorful description for room #1 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": None,
                            "ordinal_number": 1,
                            "maximum_persons": 2,
                            "price": 5_000,
                        },
                    },
                    {
                        "id": 3,
                        "user_id": 1,
                        "room_id": 2,
                        "number_of_persons": 2,
                        "check_in_dt": "2024-08-10T14:00:00Z",
                        "check_out_dt": "2024-08-22T12:00:00Z",
                        "total_cost": 110_000,
                        "room": {
                            "id": 2,
                            "name": "Room #2 of hotel #1",
                            "desc": "Colorful description for room #2 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": 2,
                            "ordinal_number": 2,
                            "maximum_persons": 3,
                            "price": 10_000,
                        },
                    },
                ],
                "Endpoint test for selecting user's bookings from the database "
                "with filter by maximum check in date",
                id="-test-3",
            ),
            pytest.param(
                {
                    "min_dt": "2024-08-01T14:00:00Z",
                    "max_dt": "2024-08-30T12:00:00Z",
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_200_OK,
                [
                    {
                        "id": 3,
                        "user_id": 1,
                        "room_id": 2,
                        "number_of_persons": 2,
                        "check_in_dt": "2024-08-10T14:00:00Z",
                        "check_out_dt": "2024-08-22T12:00:00Z",
                        "total_cost": 110_000,
                        "room": {
                            "id": 2,
                            "name": "Room #2 of hotel #1",
                            "desc": "Colorful description for room #2 of hotel #1.",
                            "hotel_id": 1,
                            "premium_level_id": 2,
                            "ordinal_number": 2,
                            "maximum_persons": 3,
                            "price": 10_000,
                        },
                    },
                ],
                "Endpoint test for selecting user's bookings from the database "
                "with filters by minimum check in date and maximum check in date",
                id="-test-4",
            ),
            pytest.param(
                {
                    "min_dt": "2024-08-30T12:00:00Z",
                    "max_dt": "2024-08-01T14:00:00Z",
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": (
                        f"The maximum date must be at least {settings.MIN_RENTAL_INTERVAL_HOURS} hours later "
                        "than the minimum."
                    ),
                    "extras": {
                        "min_dt": "2024-08-30T12:00:00+0000",
                        "max_dt": "2024-08-01T14:00:00+0000",
                    },
                },
                "Endpoint test for selecting user's bookings from the database "
                "with filters based on invalid check in and check in ranges",
                id="-test-5",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_bookings(
        self,
        query_params: dict[str, Any] | None,
        cookies: dict[str, str],
        hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        users_for_test: list[dict[str, Any]],
        bookings_for_test: list[dict[str, Any]],
        expected_status_code: int,
        expected_result: list[dict[str, Any]] | dict[str, Any],
        test_description: str,
    ):
        ic(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with (
            self.db_preparer.insert_test_data(orm_model=HotelsModel, data_for_insert=hotels_for_test),
            self.db_preparer.insert_test_data(orm_model=RoomsModel, data_for_insert=rooms_for_test),
            self.db_preparer.insert_test_data(orm_model=UsersModel, data_for_insert=users_for_test),
            self.db_preparer.insert_test_data(orm_model=BookingsModel, data_for_insert=bookings_for_test),
        ):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.get(
                    url=f"http://test{self.url}",
                    params=query_params,
                    cookies=cookies,
                )

                status_code_of_response = api_response.status_code
                ic(status_code_of_response)
                dict_of_response = api_response.json()
                ic(dict_of_response)

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
