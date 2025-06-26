from fastapi import APIRouter
from app.api.endpoints import variants, health

api_router = APIRouter()
api_router.include_router(variants.router, prefix="/variants", tags=["variants"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
