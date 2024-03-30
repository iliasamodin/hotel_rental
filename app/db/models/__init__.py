"""
All models via dynamic import.
"""

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
import os

from app.db.utils import load_model


if __name__ != "__main__":
    models_path = os.path.dirname(os.path.realpath(__file__))

    # Search and fill the list of all models
    classes_of_models: list[DeclarativeAttributeIntercept] = []
    for module_name in os.listdir(models_path):
        if module_name.endswith("model.py"):
            module_name = module_name.replace(".py", "")
            Class = load_model(package_name=__name__, module_name=module_name)
            if isinstance(Class, DeclarativeAttributeIntercept):
                classes_of_models.append(Class)
