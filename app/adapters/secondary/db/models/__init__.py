"""
All models via dynamic import.
"""

from pathlib import Path

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from app.adapters.secondary.db.base import Base
from app.tools import load_modules


models_path = Path(__file__).resolve().parent
load_modules(models_path)

classes_of_models: dict[str, DeclarativeAttributeIntercept] = {
    cls.class_.__tablename__: cls.class_
    for cls in Base.registry.mappers
    if isinstance(cls.class_, DeclarativeAttributeIntercept)
}
