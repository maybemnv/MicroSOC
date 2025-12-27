from fastapi import APIRouter
from app.api.v1.endpoints import logs, actions, dashboard

api_router = APIRouter()
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(actions.router, prefix="/actions", tags=["actions"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
