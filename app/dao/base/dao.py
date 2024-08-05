from typing import Any

from pydantic import BaseModel
from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.db.models import classes_of_models

from app.dao.base.exceptions import ModelNotFoundError
from app.dao.base.adapters import get_item_by_id, insert_item, delete_item_by_id


class BaseDAO:
    """
    DAO layer base class.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_item_by_id(
        self,
        table_name: str,
        item_id: int,
    ) -> dict[str, Any] | None:
        """
        Get item by id.

        :return: item of table.
        """

        model: DeclarativeAttributeIntercept | None = classes_of_models.get(table_name)
        if model is None:
            raise ModelNotFoundError(
                message=f"Model {table_name} not found.",
                extras={
                    "table_name": table_name,
                },
            )

        query_result_of_item: Result = await get_item_by_id(
            session=self.session,
            model=model,
            item_id=item_id,
        )
        item = query_result_of_item.mappings().fetchone()

        return item

    async def insert_item(
        self,
        table_name: str,
        item_data: dict[str, Any] | BaseModel,
    ) -> None:
        """
        Insert item into the database.

        :return: data of inserted item.
        """

        model: DeclarativeAttributeIntercept | None = classes_of_models.get(table_name)
        if model is None:
            raise ModelNotFoundError(
                message=f"Model {table_name} not found.",
                extras={
                    "table_name": table_name,
                },
            )

        query_result_of_item: Result = await insert_item(
            session=self.session,
            model=model,
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

        model: DeclarativeAttributeIntercept | None = classes_of_models.get(table_name)
        if model is None:
            raise ModelNotFoundError(
                message=f"Model {table_name} not found.",
                extras={
                    "table_name": table_name,
                },
            )

        query_result_of_item: Result = await delete_item_by_id(
            session=self.session,
            model=model,
            item_id=item_id,
        )
        item = query_result_of_item.mappings().fetchone()

        return item
