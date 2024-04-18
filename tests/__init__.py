import asyncio

from tests.db_preparer import DBPreparer


if __name__ == "__main__":
    PATH_OF_DUMP_FOR_MANUAL_TESTING = "tests/db_dumps/dump_for_manual_testing.sql"

    db_preparer = DBPreparer(path_of_test_dump=PATH_OF_DUMP_FOR_MANUAL_TESTING)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(db_preparer.setup_db())
