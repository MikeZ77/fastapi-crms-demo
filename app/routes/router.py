from fastapi import APIRouter

from app.routes import content, contracts

api_router = APIRouter()

api_router.include_router(contracts.router, prefix="/contract", tags=["contract"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
