from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

import uvicorn
import sys

from app.lifespan import lifespan
from app.settings import settings

from app.db.session import async_engine

from app.web.api.router import api_router
from app.web.api.handlers import registering_exception_handlers

from app.tools import ic, get_data_to_display_in_openapi  # noqa: F401

from app.redis.redis_controller import redis_controller

from app.admin_panel.router import registering_views
from app.admin_panel.auth import authentication_backend

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

# Adding admin panel
admin_panel = Admin(
    app=app,
    engine=async_engine,
    base_url=settings.ADMIN_PANEL_BASE_URL,
    authentication_backend=authentication_backend,
)
registering_views(admin_panel=admin_panel)

if __name__ == "__main__":
    # Adding the project root directory to the list of module paths
    sys.path.append(settings.APP_PATH)

    uvicorn.run(
        app="app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
