from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import sys

from app.lifespan import lifespan
from app.settings import settings

from app.web.api.router import api_router
from app.web.api.handlers import registering_exception_handlers

from app.tools import ic, get_data_to_display_in_openapi

from app.redis.redis_controller import redis_controller

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

# Forwarding app to redis controller
redis_controller.app = app

if __name__ == "__main__":
    # Adding the project root directory to the list of module paths
    sys.path.append(settings.APP_PATH)

    uvicorn.run(
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
