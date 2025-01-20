from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from loguru import logger
from starlette import status

import pytest

from app.adapters.primary.api.version_1.resource_manager.types import EntityNamePathParams

from tests.db_preparer import DBPreparer


@pytest.mark.asyncio
class TestGetEntitiesByFilters:
    """
    System tests for GET method
    of endpoint /resource-manager/{entity_name}.
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
        self.url = lambda path_params: app.url_path_for("get_entities_by_filters", **path_params)

    @pytest.mark.parametrize(
        argnames=(
            "path_params",
            "query_params",
            "expected_status_code",
            "expected_result",
            "test_description",
        ),
        argvalues=[
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                },
                None,
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
                "Endpoint test for selecting entities from the database",
                id="-test-1",
            ),
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                },
                {
                    "key": "wifi",
                },
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "wifi",
                        "name": "Free Wi-Fi",
                        "desc": None,
                    },
                ],
                "Endpoint test for selecting entities by filters from the database",
                id="-test-2",
            ),
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                },
                {
                    "name": "Non existent service name",
                },
                status.HTTP_200_OK,
                [],
                "Endpoint test for selecting entities by filters from the database "
                "with a filter that does not pass any of the entities in the original sample",
                id="-test-3",
            ),
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                },
                {
                    "key": "wifi",
                    "non_existent_attribute": "Any value",
                },
                status.HTTP_200_OK,
                [
                    {
                        "id": 1,
                        "key": "wifi",
                        "name": "Free Wi-Fi",
                        "desc": None,
                    },
                ],
                "Endpoint test for selecting entities by filters from the database "
                "with a filter on a non-existent entity attribute",
                id="-test-4",
            ),
            pytest.param(
                {
                    "entity_name": "non_existent_entity",
                },
                None,
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
                            "msg": "Input should be 'service_varieties', 'hotels', 'premium_level_varieties', 'rooms' "
                            "or 'images'",
                            "type": "enum",
                        },
                    ],
                },
                "Endpoint test for selecting entities from the database with a non-existent entity name",
                id="-test-5",
            ),
            pytest.param(
                {
                    "entity_name": EntityNamePathParams.ServiceVarieties.value,
                },
                {
                    "id": "Not an integer value",
                },
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                {
                    "detail": "1 validation error for service_varieties\nid\n  "
                    "Input should be a valid integer, unable to parse string as an integer "
                    "[type=int_parsing, input_value='Not an integer value', input_type=str]\n    "
                    "For further information visit https://errors.pydantic.dev/2.6/v/int_parsing",
                    "extras": [
                        {
                            "type": "int_parsing",
                            "loc": ["id"],
                            "msg": "Input should be a valid integer, unable to parse string as an integer",
                            "input": "Not an integer value",
                            "url": "https://errors.pydantic.dev/2.6/v/int_parsing",
                        },
                    ],
                },
                "Endpoint test for selecting entities by filters from the database "
                "with a filter by the value of an entity attribute with an invalid data type",
                id="-test-6",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_get_entities_by_filters(
        self,
        path_params: dict[str, Any],
        query_params: dict[str, Any] | None,
        expected_status_code: int,
        expected_result: list[dict[str, Any]] | dict[str, Any],
        test_description: str,
    ):
        logger.info(test_description)

        # Client for test requests to API
        async with self.client_maker(transport=self.transport_for_client) as client:
            api_response = await client.get(
                url=f"http://test{self.url(path_params=path_params)}",
                params=query_params,
            )

            status_code_of_response = api_response.status_code
            logger.debug(status_code_of_response)
            dict_of_response = api_response.json()
            logger.debug(dict_of_response)

        assert status_code_of_response == expected_status_code, "The returned status code is not as expected"
        assert dict_of_response == expected_result, "The data returned by the endpoint is not as expected"
