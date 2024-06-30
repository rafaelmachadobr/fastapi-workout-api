from uuid import uuid4
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi_pagination import Page, paginate, Params
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from pydantic import UUID4

from src.categories.models import CategoryModel
from src.categories.schemas import CategoryIn, CategoryOut
from src.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Create a new category",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryOut
)
async def post(
    db_session: DatabaseDependency,
    category_in: CategoryIn = Body(...)
) -> CategoryOut:
    category_out = CategoryOut(id=uuid4(), **category_in.model_dump())
    category_model = CategoryModel(**category_out.model_dump())

    try:
        db_session.add(category_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Category with name {category_in.name} already exists"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

    return category_out


@router.get(
    "/",
    summary="List all categories",
    response_model=Page[CategoryOut]
)
async def get(
    db_session: DatabaseDependency,
    name: str = Query(None, description="Filter by category name"),
    limit: int = Query(None, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the results"),
    params: Params = Depends()
) -> Page[CategoryOut]:
    query = select(CategoryModel)

    if name:
        query = query.filter(CategoryModel.name.ilike(f"%{name}%"))

    if limit:
        query = query.limit(limit)

    query = query.offset(offset)

    categories = (await db_session.execute(query)).scalars().all()

    return paginate(categories, params)


@router.get(
    "/{category_id}",
    summary="Get a category by id",
    response_model=CategoryOut
)
async def get_by_id(
    category_id: UUID4,
    db_session: DatabaseDependency
) -> CategoryOut:
    result = await db_session.execute(select(CategoryModel).filter_by(id=category_id))
    category = result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )

    return category
