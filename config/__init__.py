from fastapi import FastAPI
from config import routers
from config.db_connection import connect_db


app = FastAPI(
    title="Lucro API Promocion",
    description="API Lucro",
    version="0.1",
    redoc_url="/redoc"
)

app.include_router(
    routers.urls,
)

app.add_event_handler(
    "startup",
    connect_db
)