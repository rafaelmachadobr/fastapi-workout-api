from datetime import date
from typing import Annotated
from pydantic import Field, PositiveFloat

from src.categories.schemas import CategoryIn
from src.contrib.schemas import BaseSchema, OutMixin
from src.training_centers.schemas import TrainingCenterAthlete


class Athlete(BaseSchema):
    name: Annotated[str, Field(
        description="The name of the athlete", example="John Doe", max_length=50)]
    cpf: Annotated[str, Field(
        description="The CPF of the athlete", example="12345678901", max_length=11)]
    birth_date: Annotated[date, Field(
        description="The birth date of the athlete", example="2000-01-01")]
    weight: Annotated[PositiveFloat, Field(
        description="The weight of the athlete", example=75.5)]
    height: Annotated[PositiveFloat, Field(
        description="The height of the athlete", example=1.75)]
    sex: Annotated[str, Field(
        description="The sex of the athlete", example="M", max_length=1)]
    category: Annotated[CategoryIn, Field(
        description="The category of the athlete")]
    training_center: Annotated[TrainingCenterAthlete, Field(
        description="The training center of the athlete")]


class AthleteIn(Athlete):
    pass


class AthleteOut(AthleteIn, OutMixin):
    pass


class AthleteUpdate(BaseSchema):
    name: Annotated[str, Field(
        description="The name of the athlete", example="John Doe", max_length=50)]
