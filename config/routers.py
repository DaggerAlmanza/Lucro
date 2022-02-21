from fastapi import APIRouter

from app.api import views

urls = APIRouter()

urls.include_router(
    views.router,
    prefix="/api/v1",
)
