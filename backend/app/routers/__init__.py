from app.routers.advisory import router as advisory_router
from app.routers.suitability import router as suitability_router
from app.routers.prices import router as prices_router
from app.routers.schemes import router as schemes_router

__all__ = [
    "advisory_router",
    "suitability_router",
    "prices_router",
    "schemes_router"
]
