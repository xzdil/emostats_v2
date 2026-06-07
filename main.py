# app.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.users import register_users_route
from api.diary import register_diary_route
from db.base import BaseORM
from core.database import engine

BaseORM.metadata.create_all(bind=engine)

app = FastAPI()

register_users_route(app)
register_diary_route(app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 STARTUP
    print("App starting...")
    
    yield
    # 🔻 SHUTDOWN
    print("App shutting down...")

    app.state.db_engine.dispose()

@app.get("/", summary="Получить объект по айди")
def index():
    return {"success": True, "message": "API is working!"}