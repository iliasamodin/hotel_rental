from prometheus_fastapi_instrumentator import Instrumentator

from app.settings import settings

prometheus_instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_respect_env_var=True,
    excluded_handlers=[f"{settings.ADMIN_PANEL_BASE_URL}.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
)
