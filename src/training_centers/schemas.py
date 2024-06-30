from datetime import datetime
from typing import Annotated

from pydantic import Field, UUID4
from src.contrib.schemas import BaseSchema


class TrainingCenterIn(BaseSchema):
    name: Annotated[str, Field(
        description="The name of the training center", example="CT King", max_length=20)]
    address: Annotated[str, Field(
        description="The address of the training center", example="Street 123", max_length=60)]
    owner: Annotated[str, Field(
        description="The owner of the training center", example="John Doe", max_length=30)]


class TrainingCenterAthlete(BaseSchema):
    name: Annotated[str, Field(
        description="The name of the athlete", example="CT King", max_length=20)]


class TrainingCenterOut(TrainingCenterIn):
    id: Annotated[UUID4, Field(description="The UUID of the training center")]
