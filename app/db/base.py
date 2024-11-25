from datetime import datetime

from sqlalchemy import ColumnCollection, MetaData, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property

from app.settings import settings


# Declarative base class
class Base(DeclarativeBase):
    metadata = MetaData(schema=settings.DB_BOOKING_SCHEMA)
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }

    @classmethod
    def get_columns(cls) -> ColumnCollection:
        """
        Get columns of model.

        :return: columns.
        """

        return cls.__table__.columns

    @classmethod
    def get_hybrid_properties(cls):
        """
        Get hybrid properties of model.

        :return: hybrid properties.
        """

        hybrid_properties = [
            getattr(cls, attr) for attr, value in cls.__dict__.items()
            if isinstance(value, hybrid_property)
        ]

        return hybrid_properties
