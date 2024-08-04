from datetime import datetime
from json import JSONDecodeError
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
        "room_id": 1,
        "number_of_persons": 1,
        "check_in_dt": datetime(year=2024, month=7, day=2, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=7, day=3, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 5_000,
    },
    {
        "id": 3,
        "user_id": 1,
        "room_id": 1,
        "number_of_persons": 2,
        "check_in_dt": datetime(year=2024, month=8, day=10, hour=14, tzinfo=settings.DB_TIME_ZONE),
        "check_out_dt": datetime(year=2024, month=8, day=22, hour=12, tzinfo=settings.DB_TIME_ZONE),
        "total_cost": 55_000,
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
class TestDeleteBooking:
    """
    E2E tests for DELETE method of endpoint /bookings.
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
        self.url = lambda path_params: app.url_path_for("delete_booking", **path_params)

    @pytest.mark.parametrize(
        argnames=(
            "path_params",
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
                    "booking_id": 3,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_204_NO_CONTENT,
                None,
                "Endpoint test for deleting user's bookings from the database",
                id="-test-1",
            ),
            pytest.param(
                {
                    "booking_id": 5,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_404_NOT_FOUND,
                {
                    "detail": "The booking to be deleted is not in the database.",
                    "extras": {
                        "booking_id": 5,
                    },
                },
                "Endpoint test for deleting user's bookings from the database "
                "for a non-existent booking",
                id="-test-2",
            ),
            pytest.param(
                {
                    "booking_id": 2,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_403_FORBIDDEN,
                {
                    "detail": "The booking being canceled does not belong to the user who is deleting it.",
                    "extras": {
                        "user_id": 1,
                        "user_id_of_booking": 2,
                    },
                },
                "Endpoint test for deleting user's bookings from the database "
                "for a booking that does not belong to this user",
                id="-test-3",
            ),
            pytest.param(
                {
                    "booking_id": 1,
                },
                cookies_of_first_user,
                hotels_for_test,
                rooms_for_test,
                users_for_test,
                bookings_for_test,
                status.HTTP_405_METHOD_NOT_ALLOWED,
                {
                    "detail": "The time when the booking could be canceled has already expired.",
                    "extras": {
                        "current_dt": "2024-08-01T12:00:00+0000",
                        "latest_cancellation_dt": "2024-06-29T14:00:00+0000",
                    },
                },
                "Endpoint test for deleting user's bookings from the database "
                "for a booking for which the cancellation time has expired",
                id="-test-4",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_delete_booking(
        self,
        path_params: dict[str, Any],
        cookies: dict[str, str],
        hotels_for_test: list[dict[str, Any]],
        rooms_for_test: list[dict[str, Any]],
        users_for_test: list[dict[str, Any]],
        bookings_for_test: list[dict[str, Any]],
        expected_status_code: int,
        expected_result: dict[str, Any] | None,
        test_description: str,
    ):
        ic(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with (
            self.db_preparer.insert_test_data(orm_model=HotelsModel, data_for_insert=hotels_for_test),
            self.db_preparer.insert_test_data(orm_model=RoomsModel, data_for_insert=rooms_for_test),
            self.db_preparer.insert_test_data(orm_model=UsersModel, data_for_insert=users_for_test),
            self.db_preparer.insert_test_data(
                orm_model=BookingsModel,
                data_for_insert=bookings_for_test,
                need_to_check_deletion=False,
            ),
        ):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.delete(
                    url=f"http://test{self.url(path_params=path_params)}",
                    cookies=cookies,
                )

                status_code_of_response = api_response.status_code
                ic(status_code_of_response)

                # Duck typing of response body
                try:
                    dict_of_response = api_response.json()
                except JSONDecodeError:
                    dict_of_response = None
                ic(dict_of_response)

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
