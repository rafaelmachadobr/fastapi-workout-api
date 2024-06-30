from typing import Annotated

from pydantic import UUID4, Field
from src.contrib.schemas import BaseSchema


class CategoryIn(BaseSchema):
    name: Annotated[str, Field(
        description="The name of the category", example="Scale", max_length=10)]


class CategoryOut(CategoryIn):
    id: Annotated[UUID4, Field(description="The ID of the category")]
