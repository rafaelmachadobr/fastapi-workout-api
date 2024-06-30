from uuid import uuid4
from fastapi import APIRouter, Depends, Body, HTTPException, Query, status
from fastapi_pagination import Page, Params, paginate
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from src.contrib.dependencies import DatabaseDependency
from src.training_centers.models import TrainingCenterModel
from src.training_centers.schemas import TrainingCenterIn, TrainingCenterOut

router = APIRouter()


@router.post(
    "/",
    summary="Create a new training center",
    status_code=status.HTTP_201_CREATED,
    response_model=TrainingCenterOut
)
async def post(
    db_session: DatabaseDependency,
    training_center_in: TrainingCenterIn = Body(...)
) -> TrainingCenterOut:
    training_center_out = TrainingCenterOut(
        id=uuid4(), **training_center_in.model_dump())
    training_center_model = TrainingCenterModel(
        **training_center_out.model_dump())

    try:
        db_session.add(training_center_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Training center with name {training_center_in.name} already exists"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

    return training_center_out


@router.get(
    "/",
    summary="List all training centers",
    status_code=status.HTTP_200_OK,
    response_model=Page[TrainingCenterOut]
)
async def get(
    db_session: DatabaseDependency,
    name: str = Query(None, description="Filter by training center name"),
    limit: int = Query(None, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the results"),
    params: Params = Depends()
) -> Page[TrainingCenterOut]:
    query = select(TrainingCenterModel)

    if name:
        query = query.where(TrainingCenterModel.name.ilike(f"%{name}%"))

    if limit:
        query = query.limit(limit)

    query = query.offset(offset)

    training_centers = (await db_session.execute(query)).scalars().all()

    return paginate(training_centers, params)


@router.get(
    "/{training_center_id}",
    summary="Get a training center by id",
    status_code=status.HTTP_200_OK,
    response_model=TrainingCenterOut
)
async def get_by_id(
    training_center_id: UUID4,
    db_session: DatabaseDependency
) -> TrainingCenterOut:
    result = await db_session.execute(
        select(TrainingCenterModel).filter_by(id=training_center_id))
    training_center = result.scalars().first()

    if not training_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training center with id {training_center_id} not found"
        )

    return training_center
