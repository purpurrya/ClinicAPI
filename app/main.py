from fastapi import FastAPI
from app.database import engine, Base
from app.routers import queries_routes

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Analytics API",
    description="REST API for analytics queries",
    version="1.0.0"
)
app.include_router(queries_routes.router, prefix="/analytics", tags=["analytics"])