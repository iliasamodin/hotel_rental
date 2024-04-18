from typing import Any

from icecream import ic

import os
import toml

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

    full_path_of_pyproject = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__),
        ),
        os.pardir,
        settings.PATH_OF_PYPROJECT,
    )

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
