from datetime import date
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, computed_field, field_validator
from ..db.fake_db import passengers_db


class Passenger(BaseModel):
    id: Annotated[int, Field(strict=True)] = 0  # A cause du fake_db
    last_name: Annotated[str, Field(min_length=3, max_length=20)]
    first_name: Annotated[str, Field(min_length=3, max_length=30)]
    email: EmailStr
    birth_date: date

    @field_validator("last_name", mode="after")
    @classmethod
    def upper_last_name(cls, value: str) -> str:
        return value.upper()

    @field_validator("first_name", mode="after")
    @classmethod
    def capitalize_first_name(cls, value: str) -> str:
        return value.capitalize()

    @field_validator("birth_date", mode="after")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if date.today().year - value.year < 16:
            raise ValueError("Passenger must be at least 16 years old.")
        else:
            return value
