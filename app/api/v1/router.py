from fastapi import APIRouter
from app.api.v1.users import router as user_router

router = APIRouter(tags = ["v1"])

router.include_router(user_router, prefix = "/users")