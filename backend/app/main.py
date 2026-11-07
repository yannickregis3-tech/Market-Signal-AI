from fastapi import FastAPI

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.markets import router as markets_router
from app.api.routes.signals import router as signals_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Market research and signal decision-support API. "
        "No broker order execution is enabled."
    ),
)
app.include_router(health_router)
app.include_router(markets_router, prefix=settings.api_v1_prefix)
app.include_router(signals_router, prefix=settings.api_v1_prefix)
