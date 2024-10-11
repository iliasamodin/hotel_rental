from typing import Any, Callable

from pydantic import BaseModel
from sqlalchemy import delete, insert, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.dao.base.helpers import get_filter_by_id, get_filters_for_model


async def get_item_by_id(
    session: AsyncSession,
    orm_model: DeclarativeAttributeIntercept,
    item_id: int,
    get_query_filters: Callable = get_filter_by_id,
) -> Result:
    """
    Get the result of a query to select an item by id.

    :return: result of item query.
    """

    query_filters = get_query_filters(
        orm_model=orm_model,
        item_id=item_id,
    )

    query = (
        select(
            *orm_model.__table__.columns,
            *orm_model.get_hybrid_properties(),
        )
        .where(*query_filters)
    )

    query_result = await session.execute(query)

    return query_result


async def get_items_by_filters(
    session: AsyncSession,
    orm_model: DeclarativeAttributeIntercept,
    filters: BaseModel,
    get_query_filters: Callable = get_filters_for_model,
) -> Result:
    """
    Get the result of a query to select items by filters.

    :return: result of items query.
    """

    query_filters = get_query_filters(
        orm_model=orm_model,
        filters=filters,
    )

    query = (
        select(
            *orm_model.__table__.columns,
            *orm_model.get_hybrid_properties(),
        )
        .where(*query_filters)
    )

    query_result = await session.execute(query)

    return query_result


async def insert_item(
    session: AsyncSession,
    orm_model: DeclarativeAttributeIntercept,
    item_data: dict[str, Any] | BaseModel,
) -> Result:
    """
    Add an item to the database
    and get the result of querying the inserted item's data.

    :return: result of item query.
    """

    if isinstance(item_data, BaseModel):
        item_data: dict[str, Any] = item_data.model_dump()

    query = (
        insert(orm_model)
        .values(item_data)
        .returning(*orm_model.__table__.columns)
    )

    query_result = await session.execute(query)

    return query_result


async def delete_item_by_id(
    session: AsyncSession,
    orm_model: DeclarativeAttributeIntercept,
    item_id: int,
    get_query_filters: Callable = get_filter_by_id,
) -> Result:
    """
    Delete an item from the database
    and get the result of querying the deleted item's data.

    :return: result of item query.
    """

    query_filters = get_query_filters(
        orm_model=orm_model,
        item_id=item_id,
    )

    query = (
        delete(orm_model)
        .where(*query_filters)
        .returning(*orm_model.__table__.columns)
    )

    query_result = await session.execute(query)

    return query_result
