from app.routes.auth import router as auth_router
from app.routes.home import router as home_router
from app.routes.party import router as party_router
from app.routes.jewelry import router as jewelry_router
from app.routes.recommendations import router as recommendations_router
from app.routes.history import router as history_router

__all__ = [
    "auth_router",
    "home_router",
    "party_router",
    "jewelry_router",
    "recommendations_router",
    "history_router",
]
