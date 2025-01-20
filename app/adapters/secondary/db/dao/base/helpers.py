from pydantic import BaseModel, ConfigDict, create_model
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from loguru import logger

from app.adapters.secondary.db.dao.base.exceptions import ValidatorGenerationError
from app.core.services.base.dtos import OccurrenceFilterDTO

ignore_orm_config = ConfigDict(
    from_attributes=True,
    extra="ignore",
)
forbid_orm_config = ConfigDict(
    from_attributes=True,
    extra="forbid",
)


def get_filter_by_id(
    orm_model: DeclarativeAttributeIntercept,
    item_id: int,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters by model item id.

    :return: list of sqlalchemy filters.
    """

    query_filters = [orm_model.id == item_id]

    return query_filters


def get_pydantic_schema_by_sqlalchemy_model(
    orm_model: type[DeclarativeAttributeIntercept],
    config: ConfigDict = ignore_orm_config,
    exclude: list[str] | None = None,
    all_nullable: bool = False,
) -> BaseModel:
    """
    Get validation schema based on sqlalchemy model data.

    :return: pydantic validation scheme.
    """

    if exclude is None:
        exclude = []

    fields = {}

    for column in orm_model.__table__.columns:
        column_name = column.name
        if column_name in exclude:
            continue
        python_type: type | None = None
        if hasattr(column.type, "impl"):
            if hasattr(column.type.impl, "python_type"):
                python_type = column.type.impl.python_type
        elif hasattr(column.type, "python_type"):
            python_type = column.type.python_type

        if python_type is None:
            raise ValidatorGenerationError(
                message=f"Error generating pydantic validator from sqlalchemy model due to column {column_name}",
                extras={
                    "column_name": column_name,
                },
            )

        if all_nullable or column.nullable:
            fields[column_name] = (python_type | None, None)
        else:
            fields[column_name] = (python_type, ...)

    pydantic_schema = create_model(
        orm_model.__table__.name,
        __config__=config,
        **fields,
    )

    return pydantic_schema


def get_filters_for_model(
    orm_model: type[DeclarativeAttributeIntercept],
    filters: BaseModel | None = None,
    occurrence: OccurrenceFilterDTO | None = None,
    *args,
    **kwargs,
) -> list[BinaryExpression]:
    """
    Get sqlalchemy filters for model columns and hybrid properties.

    :return: list of sqlalchemy filters.
    """

    query_filters = []

    if filters is not None:
        for column_name, value in filters.model_dump().items():
            if hasattr(orm_model, column_name):
                if value is not None:
                    column = getattr(orm_model, column_name)
                    query_filters.append(column == value)

            else:
                logger.debug(f"Model {orm_model.__name__} has no column {column_name}.")

    if occurrence is not None:
        if hasattr(orm_model, occurrence.column_name):
            if occurrence.array:
                column = getattr(orm_model, occurrence.column_name)
                query_filters.append(column.in_(occurrence.array))

        else:
            logger.debug(f"Model {orm_model.__name__} has no column {column_name}.")

    return query_filters
