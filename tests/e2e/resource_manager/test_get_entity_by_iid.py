from json import JSONDecodeError
from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from icecream import ic
from starlette import status

import pytest

from app.web.api.resource_manager.types import EntityNamePathParams

from tests.db_preparer import DBPreparer


@pytest.mark.asyncio
class TestGetEntityByIid:
    """
    E2E tests for GET method
    of endpoint /resource-manager/{entity_name}/{iid}.
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
        self.url = lambda path_params: app.url_path_for("get_entity_by_iid", **path_params)

    @pytest.mark.parametrize(
        argnames=(
            "path_params",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                    "iid": 1,
                },
                status.HTTP_200_OK,
                {
                    "id": 1,
                    "key": "wifi",
                    "name": "Free Wi-Fi",
                    "desc": None,
                },
                "Endpoint test for selecting entity by its iid from the database",
                id="-test-1",
            ),
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                    "iid": 10_000,
                },
                status.HTTP_200_OK,
                None,
                "Endpoint test for selecting entity by its iid from the database "
                "with an id that does not exist in the DB",
                id="-test-2",
            ),
            pytest.param(
                {
                    "entity_name": "non_existent_entity",
                    "iid": 1,
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "ctx": {
                                "expected": "'service_varieties', 'hotels', 'premium_level_varieties', 'rooms' "
                                "or 'images'",
                            },
                            "input": "non_existent_entity",
                            "loc": [
                                "path",
                                "entity_name",
                            ],
                            "msg": "Input should be "
                            "'service_varieties', 'hotels', 'premium_level_varieties', 'rooms' or 'images'",
                            "type": "enum",
                        },
                    ],
                },
                "Endpoint test for selecting entity by its iid from the database "
                "with a non-existent entity name",
                id="-test-3",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_entity_by_iid(
        self,
        path_params: dict[str, Any],
        expected_status_code: int,
        expected_result: dict[str, Any] | None,
        test_description: str,
    ):
        ic(test_description)

        # Client for test requests to API
        async with self.client_maker(transport=self.transport_for_client) as client:
            api_response = await client.get(
                url=f"http://test{self.url(path_params=path_params)}",
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
