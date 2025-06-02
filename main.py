from fastapi import FastAPI
from app.database import engine, Base
from app.routers import queries_routes

app = FastAPI(
    title="Clinic API",
    description="API косметологической клиники",
    version="1.0.0",
    openapi_tags=[
        {"name": "Doctors", "description": "Статистика по врачам"},
        {"name": "Clients", "description": "Статистика по клиентам"},
        {"name": "Procedures", "description": "Статистика по процедурам"},
        {"name": "Financial", "description": "Финансовая аналитика"},
        {"name": "Operations", "description": "Операционные показатели"},
    ]
)

app.include_router(queries_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
