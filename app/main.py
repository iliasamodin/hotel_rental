from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import sys
import os

from app.lifespan import lifespan
from app.settings import settings

from app.web.api.router import api_router
from app.web.api.handlers import registering_exception_handlers

from app.tools import ic, get_data_to_display_in_openapi

openapi_params = get_data_to_display_in_openapi()

# FastAPI instance declaration
app = FastAPI(
    lifespan=lifespan,
    **openapi_params,
)
app.include_router(router=api_router, prefix=settings.API_PREFIX)
app.mount(
    path=f"/{settings.PATH_OF_MEDIA}",
    app=StaticFiles(
        directory=settings.PATH_OF_MEDIA,
    ),
    name=settings.PATH_OF_MEDIA,
)

# Registering exception handlers
registering_exception_handlers(app=app)

if __name__ == "__main__":
    # Getting the project directory 
    #   - the parent directory for the directory 
    #   in which the main.py module is located
    project_path = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__),
        ),
        os.pardir,
    )
    # Adding the project root directory to the list of module paths
    sys.path.append(project_path)

    uvicorn.run(
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
