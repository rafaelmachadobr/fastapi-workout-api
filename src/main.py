from fastapi import FastAPI
from src.routers import api_router

app = FastAPI(title="Workout API")
app.include_router(api_router)
