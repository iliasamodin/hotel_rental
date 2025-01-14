from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import sys

from app.lifespan import lifespan
from app.settings import settings

from app.adapters.primary.api.version_1.router import api_router
from app.adapters.primary.api.handlers import registering_exception_handlers
from app.adapters.primary.api.middlewares import registering_middlewares

from app.tools import ic, get_data_to_display_in_openapi  # noqa: F401
from app.logger import logger  # noqa: F401

from app.utils.redis.redis_controller import redis_controller

from app.utils.admin_panel.admin_controller import admin_panel_controller

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

# Registering exception handlers and middlewares
registering_exception_handlers(app=app)
registering_middlewares(app=app)

# Forwarding app to redis controller
redis_controller.registering_app_to_controller(app=app)

# Registering admin panel views
admin_panel_controller.registering_app_to_controller(app=app)
admin_panel_controller.registering_views()

if __name__ == "__main__":
    # Adding the project root directory to the list of module paths
    sys.path.append(settings.APP_PATH)

    uvicorn.run(
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
