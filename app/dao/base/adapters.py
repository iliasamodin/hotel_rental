from typing import Any, Callable

from pydantic import BaseModel
from sqlalchemy import delete, insert, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.dao.base.helpers import get_filter_by_id


async def get_item_by_id(
    session: AsyncSession,
    model: DeclarativeAttributeIntercept,
    item_id: int,
    get_query_filters: Callable = get_filter_by_id,
) -> Result:
    """
    Get the result of a query to select an item by id.

    :return: result of item query.
    """

    query_filters = get_query_filters(
        model=model,
        item_id=item_id,
    )

    query = (
        select(*model.__table__.columns)
        .where(*query_filters)
    )

    query_result = await session.execute(query)

    return query_result


async def insert_item(
    session: AsyncSession,
    model: DeclarativeAttributeIntercept,
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
        insert(model)
        .values(item_data)
        .returning(*model.__table__.columns)
    )

    query_result = await session.execute(query)

    return query_result


async def delete_item_by_id(
    session: AsyncSession,
    model: DeclarativeAttributeIntercept,
    item_id: int,
    get_query_filters: Callable = get_filter_by_id,
) -> Result:
    """
    Delete an item from the database
    and get the result of querying the deleted item's data.

    :return: result of item query.
    """

    query_filters = get_query_filters(
        model=model,
        item_id=item_id,
    )

    query = (
        delete(model)
        .where(*query_filters)
        .returning(*model.__table__.columns)
    )

    query_result = await session.execute(query)

    return query_result
