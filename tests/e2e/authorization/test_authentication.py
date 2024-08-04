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
]


@pytest.mark.asyncio
class TestAuthentication:
    """
    E2E tests for endpoint /authentication.
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
        self.url = app.url_path_for("authentication")

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
                    "email": "user1@example.com",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_201_CREATED,
                {
                    "token",
                    "expires",
                },
                "Endpoint test for user authentication "
                "by email and password",
                id="-test-1",
            ),
            pytest.param(
                {
                    "phone": "+7-999-999-99-97",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_201_CREATED,
                {
                    "token",
                    "expires",
                },
                "Endpoint test for user authentication "
                "by phone and password",
                id="-test-2",
            ),
            pytest.param(
                {
                    "email": "user1@example.com",
                    "phone": "+7-999-999-99-97",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_201_CREATED,
                {
                    "token",
                    "expires",
                },
                "Endpoint test for user authentication "
                "by email, phone and password",
                id="-test-3",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_authentication(
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

            keys_of_response = set(dict_of_response.keys())

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert keys_of_response == expected_result, "The data returned by the endpoint is not as expected"

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
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": "To identify the user, you need to pass the email or phone value.",
                    "extras": {
                        "email": None,
                        "phone": None,
                    },
                },
                "Endpoint test for user authentication "
                "without email and phone",
                id="-test-1",
            ),
            pytest.param(
                {
                    "email": "user2@example.com",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this email or phone number does not exist.",
                    "extras": {
                        "email": "user2@example.com",
                    },
                },
                "Endpoint test for user authentication "
                "by email and password for a user who is not in the database",
                id="-test-2",
            ),
            pytest.param(
                {
                    "phone": "+7-999-999-99-98",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this email or phone number does not exist.",
                    "extras": {
                        "phone": "+7-999-999-99-98",
                    },
                },
                "Endpoint test for user authentication "
                "by phone and password for a user who is not in the database",
                id="-test-3",
            ),
            pytest.param(
                {
                    "email": "user2@example.com",
                    "phone": "+7-999-999-99-98",
                    "password": "Password1",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "User with this email or phone number does not exist.",
                    "extras": {
                        "email": "user2@example.com",
                        "phone": "+7-999-999-99-98",
                    },
                },
                "Endpoint test for user authentication "
                "by email, phone and password for a user who is not in the database",
                id="-test-4",
            ),
            pytest.param(
                {
                    "email": "user1@example.com",
                    "password": "Password2",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "Invalid password.",
                    "extras": {
                        "password": "Password2",
                    },
                },
                "Endpoint test for user authentication "
                "by email and invalid password",
                id="-test-5",
            ),
            pytest.param(
                {
                    "phone": "+7-999-999-99-97",
                    "password": "Password2",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "Invalid password.",
                    "extras": {
                        "password": "Password2",
                    },
                },
                "Endpoint test for user authentication "
                "by phone and invalid password",
                id="-test-6",
            ),
            pytest.param(
                {
                    "email": "user1@example.com",
                    "phone": "+7-999-999-99-97",
                    "password": "Password2",
                },
                users_for_test,
                status.HTTP_409_CONFLICT,
                {
                    "detail": "Invalid password.",
                    "extras": {
                        "password": "Password2",
                    },
                },
                "Endpoint test for user authentication "
                "by email, phone and invalid password",
                id="-test-7",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_exception(
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

            assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
            assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
