from typing import Any

from fastapi import Depends, Request
from fastapi.routing import APIRouter
from starlette import status

from app.settings import settings

from app.ports.primary.resource_manager import ResourceManagerServicePort

from app.adapters.primary.api.version_1.resource_manager.types import entity_name_annotated
from app.adapters.primary.api.version_1.resource_manager.responses import (
    responses_of_getting_entity,
    responses_of_getting_entities,
)

from app.utils.redis.redis_controller import redis_controller

from app.dependencies.resource_manager import get_resource_manager_service

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
@redis_controller.cache(expire=settings.CACHE_RETENTION_TIME_SECONDS)
async def get_entities_by_filters(
    request: Request,
    entity_name: entity_name_annotated,
    service: ResourceManagerServicePort = Depends(get_resource_manager_service),
) -> list[dict[str, Any]]:
    filters = request.query_params

    entities: list[dict[str, Any]] = await service.get_entities_by_filters(
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
@redis_controller.cache(expire=settings.CACHE_RETENTION_TIME_SECONDS)
async def get_entity_by_iid(
    entity_name: entity_name_annotated,
    iid: int,
    service: ResourceManagerServicePort = Depends(get_resource_manager_service),
) -> dict[str, Any] | None:
    entity: dict[str, Any] | None = await service.get_entity_by_iid(
        entity_name=entity_name,
        iid=iid,
    )

    return entity
