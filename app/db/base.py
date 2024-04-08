from datetime import datetime

from sqlalchemy import MetaData, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings


# Declarative base class
class Base(DeclarativeBase):
    metadata = MetaData(schema=settings.DB_BOOKING_SCHEMA)
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }
