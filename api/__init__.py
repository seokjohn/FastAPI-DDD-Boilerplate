from fastapi import APIRouter

from api.auth.v1.auth import router as v1_auth_router

router = APIRouter()
router.include_router(v1_auth_router, prefix="/v1/auth", tags=["Auth"])

__all__ = ["router"]
