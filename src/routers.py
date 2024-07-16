from fastapi import APIRouter

from src.athletes.controller import router as athlete
from src.categories.controller import router as category
from src.training_centers.controller import router as training_center

api_router = APIRouter()
api_router.include_router(athlete, prefix="/athletes", tags=["athletes"])
api_router.include_router(category, prefix="/categories", tags=["categories"])
api_router.include_router(
    training_center, prefix="/training_centers", tags=["training_centers"]
)
