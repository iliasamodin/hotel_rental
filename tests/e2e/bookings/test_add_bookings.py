from datetime import datetime, timezone
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
]
bookings_for_test = [
    {
        "id": 1,
        "user_id": 1,
        "room_id": 2,
        "number_of_persons": 2,
        "check_in_dt": datetime(year=2024, month=8, day=10, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=8, day=22, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 110_000,
    },
    {
        "id": 2,
        "user_id": 1,
        "room_id": 2,
        "number_of_persons": 2,
        "check_in_dt": datetime(year=2024, month=8, day=22, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=8, day=25, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 10_000,
    },
]


@pytest.mark.asyncio
class TestAddBookings:
    """
    E2E tests for POST method of endpoint /bookings.
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
        self.url = app.url_path_for("add_booking")

    @pytest.mark.parametrize(
        argnames=(
            "body_of_request",
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
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-09-10",
                    "room_id": 1,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "id": 3,
                    "user_id": 1,
                    "room_id": 1,
                    "number_of_persons": 1,
                    "check_in_dt": "2024-07-29T14:00:00Z",
                    "check_out_dt": "2024-09-10T12:00:00Z",
                    "total_cost": 215_000,
                },
                "Endpoint test for adding booking to the database "
                "for a number with which there are no overlapping bookings.",
                id="-test-1",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-08-10",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "id": 3,
                    "user_id": 1,
                    "room_id": 2,
                    "number_of_persons": 1,
                    "check_in_dt": "2024-07-29T14:00:00Z",
                    "check_out_dt": "2024-08-10T12:00:00Z",
                    "total_cost": 120_000,
                },
                "Endpoint test for adding booking to the database "
                "on dates when there are no overlapping bookings for this number.",
                id="-test-2",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-08-25",
                    "check_out_date": "2024-09-10",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "id": 3,
                    "user_id": 1,
                    "room_id": 2,
                    "number_of_persons": 1,
                    "check_in_dt": "2024-08-25T14:00:00Z",
                    "check_out_dt": "2024-09-10T12:00:00Z",
                    "total_cost": 160_000,
                },
                "Endpoint test for adding booking to the database "
                "on dates when there are no overlapping bookings for this number.",
                id="-test-3",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-08-10",
                    "check_out_date": "2024-07-29",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "Check-out date must be later than check-in date.",
                    "extras": {
                        "check_in_date": "2024-08-10",
                        "check_out_date": "2024-07-29",
                    },
                },
                "Endpoint test for adding booking to the database "
                "with incorrect check-in and check-out dates.",
                id="-test-4",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-08-10",
                    "room_id": 2,
                    "number_of_persons": 0,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The number of person booked must be a positive number.",
                    "extras": {
                        "number_of_person_booked": 0,
                    },
                },
                "Endpoint test for adding booking to the database "
                "with incorrect number of person booked.",
                id="-test-5",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-08-10",
                    "room_id": 2,
                    "number_of_persons": 10,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The room capacity is less than the number of person booked.",
                    "extras": {
                        "room_id": 2,
                        "room_name": "Room #2 of hotel #1",
                        "maximum_persons_of_room": 3,
                        "number_of_person_booked": 10,
                    },
                },
                "Endpoint test for adding booking to the database "
                "with a number of persons exceeding the room capacity.",
                id="-test-6",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-08-11",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The room is already booked on these dates.",
                    "extras": [
                        {
                            "check_in_date": "2024-08-10",
                            "check_out_date": "2024-08-22",
                        },
                    ],
                },
                "Endpoint test for adding booking to the database "
                "with overlapping booking.",
                id="-test-7",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-08-24",
                    "check_out_date": "2024-09-10",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The room is already booked on these dates.",
                    "extras": [
                        {
                            "check_in_date": "2024-08-22",
                            "check_out_date": "2024-08-25",
                        },
                    ],
                },
                "Endpoint test for adding booking to the database "
                "with overlapping booking.",
                id="-test-8",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-08-20",
                    "check_out_date": "2024-08-24",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The room is already booked on these dates.",
                    "extras": [
                        {
                            "check_in_date": "2024-08-10",
                            "check_out_date": "2024-08-22",
                        },
                        {
                            "check_in_date": "2024-08-22",
                            "check_out_date": "2024-08-25",
                        },
                    ],
                },
                "Endpoint test for adding booking to the database "
                "with overlapping bookings.",
                id="-test-9",
            ),
            pytest.param(
                {
                    "check_in_date": "2024-07-29",
                    "check_out_date": "2024-09-10",
                    "room_id": 2,
                    "number_of_persons": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_201_CREATED,
                {
                    "detail": "The room is already booked on these dates.",
                    "extras": [
                        {
                            "check_in_date": "2024-08-10",
                            "check_out_date": "2024-08-22",
                        },
                        {
                            "check_in_date": "2024-08-22",
                            "check_out_date": "2024-08-25",
                        },
                    ],
                },
                "Endpoint test for adding booking to the database "
                "with overlapping bookings.",
                id="-test-10",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_bookings(
        self,
        body_of_request: dict[str, Any],
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
                api_response = await client.post(
                    url=f"http://test{self.url}",
                    json=body_of_request,
                    cookies=cookies,
                )

                status_code_of_response = api_response.status_code
                ic(status_code_of_response)
                dict_of_response = api_response.json()
                ic(dict_of_response)

            # Delete data added to the database by endpoint
            await self.db_preparer.delete_test_data(orm_model=BookingsModel, data_for_delete=[dict_of_response])

            assert (
                status_code_of_response == expected_status_code,
                "The status code returned by the endpoint is not as expected",
            )
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
