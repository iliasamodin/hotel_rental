from pathlib import Path
from types import ModuleType
from typing import Any

from icecream import ic
from importlib import import_module

import toml
import re

from app.settings import settings

ic.configureOutput(
    prefix="⁣\nDebug | ",
    includeContext=True,
    contextAbsPath=True,
)
if settings.MODE == "prod":
    ic.disable()


def get_project_data() -> dict[str, Any]:
    """
    Get project data from pyproject.toml file.

    :return: dict with project data.
    """

    full_path_of_pyproject = settings.PROJECT_PATH.joinpath(settings.PATH_OF_PYPROJECT)

    pyproject = toml.load(full_path_of_pyproject)

    return pyproject["tool"]["poetry"]


def get_data_to_display_in_openapi() -> dict[str, Any]:
    """
    Get project data to display in swagger.

    :return: dict with project data.
    """

    project_data = get_project_data()

    openapi_params = {
        "title": project_data["name"],
        "version": project_data["version"],
        "description": f'{project_data["description"]}'
        f"<br>{settings.MODE=}",
    }

    return openapi_params


def load_module(
    package_name: str,
    module_name: str,
) -> ModuleType:
    """
    Dynamic module import.

    :return: module.
    """

    module = import_module(f"{package_name}.{module_name}")

    return module


def load_modules(path: Path) -> list[ModuleType]:
    """
    Dynamic import for modules.

    :return: modules.
    """

    modules: list[ModuleType] = []
    for module_directory, _, names_of_modules in path.walk():
        relative_module_directory = module_directory.relative_to(settings.PROJECT_PATH)
        relative_module_directory = str(relative_module_directory).strip("\\/")
        relative_module_directory = re.sub(r"[\\/]", ".", relative_module_directory)

        for module_name in names_of_modules:
            if module_name.endswith(".py"):
                module_name = module_name.replace(".py", "")

                module = load_module(package_name=relative_module_directory, module_name=module_name)
                modules.append(module)

    return modules
