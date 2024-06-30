from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, Query, status
from pydantic import UUID4
from sqlalchemy.future import select

from src.athletes.models import AthleteModel
from src.athletes.schemas import AthleteIn, AthleteOut, AthleteUpdate
from src.categories.models import CategoryModel
from src.contrib.dependencies import DatabaseDependency
from src.training_centers.models import TrainingCenterModel

router = APIRouter()


@router.post(
    "/",
    summary="Create a new athlete",
    status_code=status.HTTP_201_CREATED,
    response_model=AthleteOut
)
async def post(
    db_session: DatabaseDependency,
    athlete_in: AthleteIn = Body(...)
) -> AthleteOut:
    category_name = athlete_in.category.name
    training_center_name = athlete_in.training_center.name

    category = (await db_session.execute(
        select(CategoryModel).filter_by(name=category_name))
    ).scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with name {category_name} not found"
        )

    training_center = (await db_session.execute(
        select(TrainingCenterModel).filter_by(name=training_center_name))
    ).scalars().first()

    if not training_center:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training center with name {training_center_name} not found"
        )

    try:
        athlete_out = AthleteOut(
            id=uuid4(), created_at=datetime.utcnow(), **athlete_in.model_dump())
        athlete_model = AthleteModel(
            **athlete_out.model_dump(exclude={"category", "training_center"}))

        athlete_model.category_id = category.pk_id
        athlete_model.training_center_id = training_center.pk_id

        db_session.add(athlete_model)
        await db_session.commit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the athlete"
        )

    return athlete_out


@router.get(
    "/",
    summary="List all athletes",
    status_code=status.HTTP_200_OK,
    response_model=list[AthleteOut]
)
async def get(
    db_session: DatabaseDependency,
    name: str = Query(None, description="Filter by athlete's name"),
    cpf: str = Query(None, description="Filter by athlete's CPF")
) -> list[AthleteOut]:
    athletes = (await db_session.execute(select(AthleteModel))).scalars().all()
    return [AthleteOut.model_validate(athlete) for athlete in athletes]


@router.get(
    "/{athlete_id}",
    summary="Get an athlete by ID",
    status_code=status.HTTP_200_OK,
    response_model=AthleteOut
)
async def get_by_id(
    athlete_id: UUID4,
    db_session: DatabaseDependency
) -> AthleteOut:
    athlete = (await db_session.execute(
        select(AthleteModel).filter_by(id=athlete_id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )

    return athlete


@router.patch(
    "/{athlete_id}",
    summary="Update an athlete by ID",
    status_code=status.HTTP_200_OK,
    response_model=AthleteOut
)
async def patch(
    athlete_id: UUID4,
    db_session: DatabaseDependency,
    athlete_up: AthleteUpdate = Body(...)
) -> AthleteOut:
    athlete = (await db_session.execute(
        select(AthleteModel).filter_by(id=athlete_id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )

    athlete_update = athlete_up.model_dump(exclude_unset=True)

    for key, value in athlete_update.items():
        setattr(athlete, key, value)

    await db_session.commit()
    await db_session.refresh(athlete)

    return athlete


@router.delete(
    "/{athlete_id}",
    summary="Delete an athlete by ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    athlete_id: UUID4,
    db_session: DatabaseDependency
) -> None:
    athlete: AthleteOut = (
        await db_session.execute(select(AthleteModel).filter_by(id=athlete_id))
    ).scalars().first()

    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} not found"
        )

    await db_session.delete(athlete)
    await db_session.commit()
