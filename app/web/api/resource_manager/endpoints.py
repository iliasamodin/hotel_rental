from typing import Any

from fastapi import Depends, Request
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.services.resource_manager.service import ResourceManagerService

from app.services.check.services import get_session_maker

from app.web.api.resource_manager.types import entity_name_annotated
from app.web.api.resource_manager.responses import responses_of_getting_entity, responses_of_getting_entities

router = APIRouter(prefix="/resource-manager")


@router.get(
    path="/{entity_name}",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_entities,
    summary="Get entities by filters.",
    description="Sampling filters are passed through query-parameters "
    "and are validated individually for each entity.<br>"
    "Query-parameters provide the ability to filter elements based on equality with the filter value.<br>"
    "Other comparison operators are not supported.",
)
async def get_entities_by_filters(
    request: Request,
    entity_name: entity_name_annotated,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> list[dict[str, Any]]:
    filters = request.query_params

    resource_manager_service = ResourceManagerService(session_maker=session_maker)
    entities: list[dict[str, Any]] = await resource_manager_service.get_entities_by_filters(
        entity_name=entity_name,
        filters=filters,
    )

    return entities


@router.get(
    path="/{entity_name}/{iid}",
    status_code=status.HTTP_200_OK,
    responses=responses_of_getting_entity,
    summary="Get entity by iid.",
)
async def get_entity_by_iid(
    entity_name: entity_name_annotated,
    iid: int,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> dict[str, Any] | None:
    resource_manager_service = ResourceManagerService(session_maker=session_maker)
    entity: dict[str, Any] | None = await resource_manager_service.get_entity_by_iid(
        entity_name=entity_name,
        iid=iid,
    )

    return entity
