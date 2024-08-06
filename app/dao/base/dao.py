from typing import Any

from pydantic import BaseModel
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.db.models import classes_of_models

from app.dao.base.exceptions import ModelNotFoundError
from app.dao.base.adapters import get_item_by_id, get_items_by_filters, insert_item, delete_item_by_id
from app.dao.base.helpers import get_pydantic_schema_by_sqlalchemy_model


class BaseDAO:
    """
    DAO layer base class.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    def _get_model_by_table_name(self, table_name: str) -> DeclarativeAttributeIntercept:
        """
        Get model by table name.

        :return: model of table.
        """

        orm_model: DeclarativeAttributeIntercept | None = classes_of_models.get(table_name)
        if orm_model is None:
            raise ModelNotFoundError(
                message=f"Model {table_name} not found.",
                extras={
                    "table_name": table_name,
                },
            )

        return orm_model

    async def get_item_by_id(
        self,
        table_name: str,
        item_id: int,
    ) -> dict[str, Any] | None:
        """
        Get item by id.

        :return: item of table.
        """

        orm_model = self._get_model_by_table_name(table_name=table_name)

        query_result_of_item: Result = await get_item_by_id(
            session=self.session,
            orm_model=orm_model,
            item_id=item_id,
        )
        item = query_result_of_item.mappings().fetchone()

        return item

    async def get_items_by_filters(
        self,
        table_name: str,
        filters: dict[str, str],
    ) -> list[dict[str, Any]]:
        """
        Get items by filters.

        :return: items of table.
        """

        orm_model = self._get_model_by_table_name(table_name=table_name)

        # Validate query filters
        #   for compliance with the column types of the table
        #   from which the selection is made
        pydantic_schema: BaseModel = get_pydantic_schema_by_sqlalchemy_model(
            orm_model=orm_model,
            all_nullable=True,
        )
        filters: BaseModel = pydantic_schema.model_validate(filters)

        query_result_of_items: Result = await get_items_by_filters(
            session=self.session,
            orm_model=orm_model,
            filters=filters,
        )
        items = query_result_of_items.mappings().fetchall()

        return items

    async def insert_item(
        self,
        table_name: str,
        item_data: dict[str, Any] | BaseModel,
    ) -> None:
        """
        Insert item into the database.

        :return: data of inserted item.
        """

        orm_model = self._get_model_by_table_name(table_name=table_name)

        query_result_of_item: Result = await insert_item(
            session=self.session,
            orm_model=orm_model,
            item_data=item_data,
        )
        item = query_result_of_item.mappings().fetchone()

        return item

    async def delete_item_by_id(
        self,
        table_name: str,
        item_id: int,
    ) -> dict[str, Any]:
        """
        Delete item by id.

        :return: data of deleted item.
        """

        orm_model = self._get_model_by_table_name(table_name=table_name)

        query_result_of_item: Result = await delete_item_by_id(
            session=self.session,
            orm_model=orm_model,
            item_id=item_id,
        )
        item = query_result_of_item.mappings().fetchone()

        return item
