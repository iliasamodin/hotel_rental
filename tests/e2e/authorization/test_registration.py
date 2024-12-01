from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic
from starlette import status

import pytest

from app.db.models.users_model import UsersModel

from app.services.authorization.helpers import get_password_hash

from tests.db_preparer import DBPreparer

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


@pytest.mark.asyncio
class TestRegistration:
    """
    E2E tests for endpoint /registration.
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
        self.url = app.url_path_for("registration")

    @pytest.mark.parametrize(
        argnames=(
            "body_of_request",
            "users_for_test",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_201_CREATED,
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "id": 3,
                    "is_admin": False,
                },
                "Endpoint test for registering a user and adding him to the database",
                id="-test-1",
            ),
            pytest.param(
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Freddie",
                    "last_name": "Mercury",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_201_CREATED,
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Freddie",
                    "last_name": "Mercury",
                    "id": 3,
                    "is_admin": False,
                },
                "Endpoint test for registering a user with first name, last name and password "
                "that is already associated with another user in the database",
                id="-test-2",
            ),
            pytest.param(
                {
                    "email": "user3example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "ctx": {
                                "reason": "The email address is not valid. It must have exactly one @-sign.",
                            },
                            "input": "user3example.com",
                            "loc": [
                                "body",
                                "email",
                            ],
                            "msg": "value is not a valid email address: The email address is not valid. "
                            "It must have exactly one @-sign.",
                            "type": "value_error",
                        },
                    ],
                },
                "Endpoint test for registering a user with invalid email",
                id="-test-3",
            ),
            pytest.param(
                {
                    "email": "user3@example.com",
                    "phone": "+7-ggg-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "input": "+7-ggg-999-99-99",
                            "loc": [
                                "body",
                                "phone",
                            ],
                            "msg": "value is not a valid phone number",
                            "type": "value_error",
                        },
                    ],
                },
                "Endpoint test for registering a user with invalid phone",
                id="-test-4",
            ),
            pytest.param(
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password 3",
                },
                users_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "input": "Password 3",
                            "loc": [
                                "body",
                                "password",
                            ],
                            "msg": "value is not a valid password",
                            "type": "value_error",
                        },
                    ],
                },
                "Endpoint test for registering a user with invalid password",
                id="-test-5",
            ),
            pytest.param(
                {
                    "email": "user1@example.com",
                    "phone": "+7-999-999-99-99",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this email already exists.",
                    "extras": {
                        "email": "user1@example.com",
                    },
                },
                "Endpoint test for registering a user with email "
                "that is already associated with another user in the database",
                id="-test-6",
            ),
            pytest.param(
                {
                    "email": "user3@example.com",
                    "phone": "+7-999-999-99-97",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this phone already exists.",
                    "extras": {
                        "phone": "+7-999-999-99-97",
                    },
                },
                "Endpoint test for registering a user with phone "
                "that is already associated with another user in the database",
                id="-test-7",
            ),
            pytest.param(
                {
                    "email": "user1@example.com",
                    "phone": "+7-999-999-99-97",
                    "first_name": "Till",
                    "last_name": "Lindemann",
                    "password": "Password3",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this email already exists.",
                    "extras": {
                        "email": "user1@example.com",
                    },
                },
                "Endpoint test for registering a user with email and phone "
                "that is already associated with another user in the database",
                id="-test-8",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_registration(
        self,
        body_of_request: dict[str, str],
        users_for_test: list[dict[str, Any]],
        expected_status_code: int,
        expected_result: dict[str, Any],
        test_description: str,
    ):
        ic(test_description)

        # Inserting test data into the database before each test
        #   and deleting this data after each test
        async with self.db_preparer.insert_test_data(orm_model=UsersModel, data_for_insert=users_for_test):
            # Client for test requests to API
            async with self.client_maker(transport=self.transport_for_client) as client:
                api_response = await client.post(
                    url=f"http://test{self.url}",
                    json=body_of_request,
                )

                status_code_of_response = api_response.status_code
                ic(status_code_of_response)
                dict_of_response = api_response.json()
                ic(dict_of_response)

            # Delete data added to the database by endpoint
            await self.db_preparer.delete_test_data(orm_model=UsersModel, data_for_delete=[dict_of_response])

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
