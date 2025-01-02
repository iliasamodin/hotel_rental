from datetime import datetime
from logging import Formatter
from pathlib import Path

from loguru import logger
from orjson import orjson

from app.settings import settings


class CustomFormatter(Formatter):
    """
    Custom log formatter.
    """

    def serializer_for_file(self, record: dict) -> dict:
        """
        Serialize log record to JSON.

        :return: JSON with log record.
        """

        subset = {
            "timestamp": datetime.strftime(record["time"], settings.LOG_DATE_FMT),
            "level": record["level"].name,
            "message": record["message"],
            "file": record["file"].name,
            "line": record["line"],
        }

        json_log = orjson.dumps(
            subset,
            option=orjson.OPT_OMIT_MICROSECONDS,
        ).decode("U8")

        return json_log

    def format(self, record: dict) -> str:
        """
        Format log record.

        :return: template of log record.
        """

        serialized_log = self.serializer_for_file(record)
        record["extra"].setdefault("serialized_message", serialized_log)

        fmt = "{extra[serialized_message]}\n"

        return fmt

    def __call__(self, record: dict) -> str:
        """
        Format log record.

        :return: template of log record.
        """

        fmt = self.format(record)

        return fmt


logger.add(
    sink=Path(settings.LOG_PATH).absolute(),
    format=CustomFormatter(),
    level=settings.LOG_LEVEL,
)
