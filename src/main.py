from fastapi import FastAPI
from fastapi_pagination import add_pagination
from src.routers import api_router

app = FastAPI(title="Workout API")

app.include_router(api_router)

add_pagination(app)
