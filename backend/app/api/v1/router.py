from fastapi import APIRouter

from app.api.v1.routes import health, imports

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(imports.router)
