from typing import Callable
from sqlalchemy import select
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
