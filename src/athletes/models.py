from datetime import date, datetime
from sqlalchemy import Date, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.contrib.models import BaseModel


class AthleteModel(BaseModel):
    __tablename__ = 'athletes'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    sex: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now)
    category: Mapped["CategoryModel"] = relationship(
        back_populates="athletes", lazy='selectin')
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.pk_id"))
    training_center: Mapped["TrainingCenterModel"] = relationship(
        back_populates="athletes", lazy='selectin')
    training_center_id: Mapped[int] = mapped_column(
        ForeignKey("training_centers.pk_id"))
