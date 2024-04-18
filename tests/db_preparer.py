from typing import Any

from contextlib import asynccontextmanager

from sqlalchemy import text, delete, insert, Column, Result, and_, or_, ColumnElement
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import IntegrityError, DBAPIError, ProgrammingError
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from sqlalchemy.sql.elements import BinaryExpression
from icecream import ic

import pytest
import sqlparse
import asyncio
import os

from app.settings import settings

from app.db.session import get_async_session_maker
from app.db.base import Base
from app.db.models import classes_of_models


class DBPreparer:
    def __init__(
        self, 
        session_maker: sessionmaker = get_async_session_maker(), 
        path_of_test_dump: str = settings.PATH_OF_TEST_DUMP,
        base_class_of_models: DeclarativeBase = Base,
        classes_of_models: list[DeclarativeAttributeIntercept] = classes_of_models,
    ):
        self.session_maker = session_maker
        self.engine = session_maker.kw["bind"]

        self.full_path_of_test_dump = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__),
            ),
            os.pardir,
            path_of_test_dump,
        )

        self.base_class_of_models = base_class_of_models
        self.classes_of_models = classes_of_models

    async def clean_table(
        self,
        orm_model: DeclarativeAttributeIntercept,
    ) -> None:
        """
        Clear table in the database.
        """

        async with self.session_maker.begin() as session:
            await session.execute(delete(orm_model))

    async def load_test_dump(self) -> None:
        """
        Load dump from file to database.
        """

        try:
            async with self.session_maker() as session:
                with open(self.full_path_of_test_dump, "r") as sql_file:
                    sql_commands = sqlparse.parsestream(sql_file)
                    for command in sql_commands:
                        if command.get_type() == "INSERT":
                            await session.execute(text(str(command)))
                            await session.commit()

        except IntegrityError as error:
            ic(f"The database is already full:\n{error._sql_message}")
        except ProgrammingError as error:
            pytest.exit(f"Error in startup conditions:\n{error._sql_message}")
        except DBAPIError as error:
            pytest.exit(f"Error in startup conditions:\n{error._sql_message}")

    async def setup_db(
        self,
        clean_tables: bool = True,
    ) -> None:
        """
        Prepare the database for tests.
        """

        if clean_tables:
            tasks = []
            for class_of_model in self.classes_of_models:
                tasks.append(
                    asyncio.create_task(
                        self.clean_table(
                            orm_model=class_of_model,
                        ),
                    ),
                )
            for task in tasks:
                await task

        await self.load_test_dump()

        tasks = []
        for class_of_model in self.classes_of_models:
            tasks.append(
                asyncio.create_task(
                    self.restore_seq_in_table(
                        orm_model=class_of_model,
                    ),
                ),
            )
        for task in tasks:
            await task

    async def recreate_table(
        self,
        orm_model: DeclarativeAttributeIntercept,
    ) -> None:
        """
        Recreate table in the database.
        """

        async with self.engine.begin() as connect:
            await connect.run_sync(
                self.base_class_of_models.metadata.drop_all, 
                tables=[orm_model.__table__],
            )
            await connect.run_sync(
                self.base_class_of_models.metadata.create_all, 
                tables=[orm_model.__table__],
            )

    async def restore_seq_in_table(
        self,
        orm_model: DeclarativeAttributeIntercept,
    ) -> tuple[tuple[Column], int | None]:
        """
        Restore the sequence in the table.

        :return: primary key of the model 
        and current value of the restored sequence.
        """

        pk_of_orm_model = inspect(orm_model).primary_key

        current_value_of_seq = None
        if len(pk_of_orm_model) == 1:
            column_of_pk: Column = pk_of_orm_model[0]
            target_table = f"{orm_model.metadata.schema}.{orm_model.__tablename__}"

            async with self.session_maker.begin() as session:
                query = text(
                    f"""
                    SELECT setval(
                        '{target_table}_{column_of_pk.name}_seq',
                        COALESCE(
                            (SELECT MAX({column_of_pk.name}) FROM {target_table}), 
                            1
                        )
                    );
                    """
                )

                query_result: Result = await session.execute(query)
                current_value_of_seq = query_result.fetchone()[0]

        return pk_of_orm_model, current_value_of_seq

    @asynccontextmanager
    async def insert_test_data(
        self,
        orm_model: DeclarativeAttributeIntercept,
        data_for_insert: list[dict[str, Any]],
        need_to_delete: bool = True,
        need_to_check_deletion: bool = True,
    ):
        """
        Add data to the database before the test 
        and delete it after the test.

        :return: list of row's indices.
        """

        pk_of_orm_model, _ = await self.restore_seq_in_table(orm_model=orm_model)

        async with self.session_maker() as session:
            # Add rows to the database
            insert_query = insert(orm_model).values(data_for_insert).returning(*pk_of_orm_model)
            insert_query_result = await session.execute(insert_query)
            await session.commit()

            maps_of_pks_and_values_for_new_rows = insert_query_result.mappings().fetchall()

            try:
                yield maps_of_pks_and_values_for_new_rows

            finally:
                if need_to_delete:
                    # Preparing filters to remove test data from database
                    delete_query_filters: list[ColumnElement[bool]] = []
                    for map_of_pks_and_values_for_new_row in maps_of_pks_and_values_for_new_rows:
                        filters_for_deleting_the_row: list[BinaryExpression] = []
                        for column_of_pk in pk_of_orm_model:
                            filters_for_deleting_the_row.append(
                                column_of_pk == map_of_pks_and_values_for_new_row.get(column_of_pk.name)
                            )

                        delete_query_filters.append(and_(*filters_for_deleting_the_row))

                    # Delete rows from database
                    delete_query = (
                        delete(orm_model)
                        .where(or_(*delete_query_filters))
                        .returning(*pk_of_orm_model)
                    )
                    delete_query_result = await session.execute(delete_query)
                    await session.commit()

                    maps_of_pks_and_values_for_deleted_rows = delete_query_result.mappings().fetchall()

                    # Verifying that only test data has been removed 
                    #   from the database
                    if (
                        need_to_check_deletion
                        and maps_of_pks_and_values_for_deleted_rows != maps_of_pks_and_values_for_new_rows
                    ):
                        pytest.exit("The preparer was unable to remove all test data")
