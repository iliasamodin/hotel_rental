from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


def get_filter_by_id(
    model: DeclarativeAttributeIntercept,
    item_id: int,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters by model item id.

    :return: list of sqlalchemy filters.
    """

    query_filters = [model.id == item_id]

    return query_filters
